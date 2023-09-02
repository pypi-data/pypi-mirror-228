import asyncio
import inspect
import typing
from enum import StrEnum
from typing import List

import aiohttp
import pytest
import requests
from pydantic import BaseModel

from ..api_types import (
    CreateCycleRequest,
    CreateCycleResponse,
    LogTestTags,
    TestCaseStatus,
)
from ..context_manager import GlooTagsCtx, GlooLoggerCtx
from ..env import ENV
from ..logging import logger
import os


U = typing.TypeVar("U", bound=BaseModel)

GLOO_CYCLE_ID: typing.Optional[str] = None


class GlooTestCaseBase(typing.TypedDict):
    name: str


T = typing.TypeVar("T", bound=GlooTestCaseBase)

session = requests.Session()


class TestAPIWrapper:
    def __init__(self) -> None:
        self.base_url = ENV.GLOO_BASE_URL
        key = ENV.GLOO_APP_SECRET
        self.session = session

        self.headers = {
            "Content-Type": "application/json",
        }
        if key:
            self.headers["Authorization"] = f"Bearer {key}"

    def global_gloo_cycle_id(self) -> str:
        global GLOO_CYCLE_ID
        if GLOO_CYCLE_ID is None:
            GLOO_CYCLE_ID = self.create_cycle_id(
                create_cycle_request=CreateCycleRequest(project_id=ENV.GLOO_APP_ID)
            )
        return GLOO_CYCLE_ID

    def post(
        self,
        url: str,
        data: typing.Dict[str, typing.Any],
        model: typing.Optional[typing.Type[U]] = None,
    ) -> typing.Union[U, typing.Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/{url}", json=data, headers=self.headers
            )
            if response.status_code != 200:
                raise Exception(
                    f"GlooTest Error: /{url} {response.status_code} {response.text}"
                )
            if model:
                return model.model_validate_json(response.text)
            return response.json()
        except Exception as e:
            raise e

    def create_cycle_id(self, create_cycle_request: CreateCycleRequest) -> str:
        response = self.post(
            "tests/create-cycle",
            create_cycle_request.model_dump(by_alias=True),
            CreateCycleResponse,
        )
        if not response:
            raise Exception(
                "Failed to register test with Gloo Services. Did you forget to run init_gloo with a project_id anywhere in the call path?"  # noqa: E501
            )
        print(f"\033[94mSee test results at: {response.dashboard_url}\033[0m")
        return response.test_cycle_id

    def create_test_cases(
        self, dataset_name: str, case_name: str, case_args_name: List[str]
    ) -> None:
        case_args_dict = [{"name": arg} for arg in case_args_name]
        self.post(
            "tests/create-case",
            {
                "project_id": ENV.GLOO_APP_ID,
                "test_cycle_id": self.global_gloo_cycle_id(),
                "test_dataset_name": dataset_name,
                "test_name": case_name,
                "test_case_args": case_args_dict,
            },
        )

    def update_test_case(
        self,
        dataset_name: str,
        case_name: str,
        case_args_name: str,
        status: TestCaseStatus,
        result_data: typing.Any,
        error_data: typing.Any,
    ) -> None:
        self.post(
            "tests/update",
            {
                "project_id": ENV.GLOO_APP_ID,
                "test_cycle_id": self.global_gloo_cycle_id(),
                "test_dataset_name": dataset_name,
                "test_case_definition_name": case_name,
                "test_case_arg_name": case_args_name,
                "status": status,
                "result_data": result_data,
                "error_data": error_data,
            },
        )


# def pytest_addoption(parser):
#     parser.addoption(
#         "--myoption", action="store", default="default_value", help="My custom option"
#     )


def pytest_configure(config: pytest.Config) -> None:
    config.pluginmanager.register(MyPlugin(), "pytest_gloo")


dataset_name_key = pytest.StashKey[str]()
case_name_key = pytest.StashKey[str]()
test_name_key = pytest.StashKey[str]()


# See https://docs.pytest.org/en/7.1.x/_modules/_pytest/hookspec.html#pytest_runtestloop
class MyPlugin:
    # wrapper ensures we can yield to other hooks
    # this one just sets the context but doesnt actually run
    # the test. It lets the "default" hook run the test.
    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_call(
        self, item: pytest.Item
    ) -> typing.Generator[None, None, None]:
        global GLOO_CYCLE_ID
        dataset_name = item.stash[dataset_name_key]
        case_name = item.stash[case_name_key]
        test_name = item.stash[test_name_key]
        test_tags = LogTestTags(
            test_case_arg_name=case_name,
            test_case_name=test_name,
            test_cycle_id=GLOO_CYCLE_ID or "no_cycle_id",
            test_dataset_name=dataset_name,
        )

        with GlooTagsCtx(
            **test_tags.model_dump(by_alias=True),
        ):
            yield

    def pytest_collection_modifyitems(
        self,
        session: pytest.Session,
        config: pytest.Config,
        items: typing.List[pytest.Item],
    ) -> None:
        # set the STAGE env variable
        os.environ["GLOO_STAGE"] = "test"
        api_wrapper = TestAPIWrapper()
        global GLOO_CYCLE_ID
        GLOO_CYCLE_ID = api_wrapper.create_cycle_id(
            CreateCycleRequest(project_id=ENV.GLOO_APP_ID)
        )
        dataset_cases: typing.Dict[str, typing.List[str]] = {}

        for item in items:
            # Get the name of the test function
            case_name = item.name
            # Get the name of the test class if exists
            dataset_name = item.parent.name if item.parent else "NoClass"

            # sanitize names. TODO.. make this more robust and handle more cases
            dataset_name = dataset_name.replace("[", "_").replace("]", "")
            case_name = case_name.replace("[", "_").replace("]", "")

            # Add case_name to the corresponding dataset
            if dataset_name not in dataset_cases:
                dataset_cases[dataset_name] = []
            dataset_cases[dataset_name].append(case_name)

            item.stash[dataset_name_key] = dataset_name
            item.stash[case_name_key] = case_name
            item.stash[test_name_key] = "test"

        # Create a test case with the collected information for each unique dataset_name
        for dataset_name, case_names in dataset_cases.items():
            api_wrapper.create_test_cases(dataset_name, "test", case_names)

    def pytest_runtest_makereport(
        self, item: pytest.Item, call: pytest.CallInfo[typing.Any]
    ) -> None:
        if call.when == "call":
            api_wrapper = TestAPIWrapper()
            dataset_name = item.stash[dataset_name_key]
            case_name = item.stash[case_name_key]
            status = (
                TestCaseStatus.PASSED if call.excinfo is None else TestCaseStatus.FAILED
            )
            result_data = call.result if call.excinfo is None else None
            error_data = str(call.excinfo.value) if call.excinfo else None

            api_wrapper.update_test_case(
                dataset_name,
                "test",
                case_name,
                status,
                {"result": result_data},
                {
                    "error": error_data,
                },
            )
