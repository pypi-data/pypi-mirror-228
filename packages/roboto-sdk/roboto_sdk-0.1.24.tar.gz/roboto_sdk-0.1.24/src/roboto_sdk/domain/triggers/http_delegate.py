#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Any, Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    headers_for_org_and_user,
)
from ...query import (
    ConditionType,
    QuerySpecification,
)
from ...serde import pydantic_jsonable_dict
from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)
from .http_resources import CreateTriggerRequest
from .trigger_delegate import TriggerDelegate
from .trigger_http_resources import (
    UpdateTriggerRequest,
)
from .trigger_record import TriggerRecord


class TriggerHttpDelegate(TriggerDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_trigger(
        self,
        name: str,
        action_name: str,
        required_inputs: list[str],
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,  # A Roboto user_id
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
        condition: Optional[ConditionType] = None,
    ) -> TriggerRecord:
        url = self.__http_client.url("v1/triggers")
        headers = headers_for_org_and_user(
            org_id=org_id,
            user_id=created_by,
            additional_headers={"Content-Type": "application/json"},
        )

        request_body = CreateTriggerRequest(
            name=name,
            action_name=action_name,
            required_inputs=required_inputs,
            compute_requirement_overrides=compute_requirement_overrides,
            container_parameter_overrides=container_parameter_overrides,
            condition=condition,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url, data=pydantic_jsonable_dict(request_body), headers=headers
            )

        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> TriggerRecord:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = headers_for_org_and_user(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=headers)

        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_triggers(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[TriggerRecord]:
        url = self.__http_client.url("v1/triggers/query")
        post_body = pydantic_jsonable_dict(query, exclude_none=True)
        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=post_body,
                headers=headers_for_org_and_user(
                    org_id=org_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )

        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                TriggerRecord.parse_obj(trigger) for trigger in unmarshalled["items"]
            ],
            next_token=unmarshalled.get("next_token"),
        )

    def delete_trigger(self, name: str, org_id: str) -> None:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = headers_for_org_and_user(org_id=org_id)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url, headers=headers)

    def update_trigger(
        self,
        name: str,
        org_id: str,
        updates: dict[str, Any],
        updated_by: Optional[str] = None,
    ) -> TriggerRecord:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = headers_for_org_and_user(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url=url,
                headers=headers,
                data=pydantic_jsonable_dict(UpdateTriggerRequest(updates=updates)),
            )

        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))
