#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Any

import pydantic


class UpdateTriggerRequest(pydantic.BaseModel):
    updates: dict[str, Any]
