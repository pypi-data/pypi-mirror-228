#  Copyright (c) 2023 Roboto Technologies, Inc.

import datetime
from distutils.version import StrictVersion
import importlib.metadata
import sys
from typing import Optional

import pydantic

from roboto_sdk.http import HttpClient
from roboto_sdk.profile import RobotoProfile
from roboto_sdk.time import utcnow


class CLIState(pydantic.BaseModel):
    last_checked_version: Optional[datetime.datetime]


def check_last_update(profile: RobotoProfile):
    roboto_tmp_dir = profile.config_dir / "tmp"
    roboto_tmp_dir.mkdir(parents=True, exist_ok=True)
    cli_state_file = roboto_tmp_dir / "cli_state.json"

    state = CLIState(last_checked_version=None)
    if cli_state_file.is_file():
        state = CLIState.parse_file(cli_state_file)

    if (
        state.last_checked_version is None
        or (utcnow() - datetime.timedelta(hours=1)) > state.last_checked_version
    ):
        version = importlib.metadata.version("roboto_sdk")
        http = HttpClient()

        state.last_checked_version = utcnow()

        versions = list(
            http.get(url="https://pypi.org/pypi/roboto-sdk/json")
            .from_json(json_path=["releases"])
            .keys()
        )
        versions.sort(key=StrictVersion)

        if version != versions[-1]:
            print(
                f"A newer version of 'roboto_sdk' exists! You're running {version},"
                + f" the latest is {versions[-1]}. You can upgrade by running:",
                file=sys.stderr,
            )
            print("pip install --upgrade roboto_sdk", file=sys.stderr)

        cli_state_file.write_text(state.json())
