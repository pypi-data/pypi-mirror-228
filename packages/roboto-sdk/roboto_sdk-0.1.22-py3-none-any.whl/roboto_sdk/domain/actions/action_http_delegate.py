from typing import Any, Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    headers_for_org_and_user,
)
from ...logging import default_logger
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from ...updates import UpdateCondition
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_delegate import ActionDelegate
from .action_http_resources import (
    ActionRecordUpdates,
    CreateActionRequest,
    UpdateActionRequest,
)
from .action_record import ActionRecord

logger = default_logger()


class ActionHttpDelegate(ActionDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def headers(
        self, org_id: Optional[str] = None, user_id: Optional[str] = None
    ) -> dict[str, str]:
        return headers_for_org_and_user(
            org_id=org_id,
            user_id=user_id,
            additional_headers={"Content-Type": "application/json"},
        )

    def create_action(
        self,
        name: str,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        description: Optional[str] = None,
        uri: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        compute_requirements: Optional[ComputeRequirements] = None,
        container_parameters: Optional[ContainerParameters] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions"
        request_body = CreateActionRequest(
            name=name,
            description=description,
            uri=uri,
            metadata=metadata,
            tags=tags,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(org_id, created_by),
            )

        return ActionRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_action_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{name}"

        with RobotoHttpExceptionParse():
            res = self.__http_client.get(url, headers=self.headers(org_id))

        return ActionRecord.parse_obj(res.from_json(json_path=["data"]))

    def delete_action(self, record: ActionRecord) -> None:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}"
        with RobotoHttpExceptionParse():
            self.__http_client.delete(url, headers=self.headers(record.org_id))

    def query_actions(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[ActionRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/query"
        post_body = pydantic_jsonable_dict(query, exclude_none=True)
        with RobotoHttpExceptionParse():
            res = self.__http_client.post(
                url,
                data=post_body,
                headers=self.headers(org_id),
            )
        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                ActionRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def update(
        self,
        record: ActionRecord,
        updates: dict[str, Any],
        conditions: Optional[list[UpdateCondition]],
        updated_by: Optional[str] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}"
        request_body = UpdateActionRequest(
            updates=ActionRecordUpdates.parse_obj(updates),
            conditions=conditions if conditions is not None else [],
        )
        with RobotoHttpExceptionParse():
            res = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(
                    request_body, exclude_unset=True, exclude_none=True
                ),
                headers=self.headers(record.org_id, updated_by),
            )

        return ActionRecord.parse_obj(res.from_json(json_path=["data"]))
