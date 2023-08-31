from typing import Any, Optional

import pydantic

from ...updates import UpdateCondition
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)


class CreateActionRequest(pydantic.BaseModel):
    # Required
    name: str

    # Optional
    description: Optional[str] = None
    uri: Optional[str] = None
    metadata: Optional[dict[str, Any]] = pydantic.Field(default_factory=dict)
    tags: Optional[list[str]] = pydantic.Field(default_factory=list)
    compute_requirements: Optional[ComputeRequirements] = None
    container_parameters: Optional[ContainerParameters] = None


class QueryActionsRequest(pydantic.BaseModel):
    filters: dict[str, Any] = pydantic.Field(default_factory=dict)

    class Config:
        extra = "forbid"


class ActionRecordUpdates(pydantic.BaseModel):
    description: Optional[str] = None
    uri: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    tags: Optional[list[str]] = None
    compute_requirements: Optional[ComputeRequirements] = None
    container_parameters: Optional[ContainerParameters] = None

    class Config:
        extra = "forbid"


class UpdateActionRequest(pydantic.BaseModel):
    updates: ActionRecordUpdates
    conditions: Optional[list[UpdateCondition]] = None
