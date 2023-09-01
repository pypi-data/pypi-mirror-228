#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import shlex
import subprocess
import sys

from ...auth import Permissions
from ...image_registry import ImageRegistry
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def pull(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    image_registry = ImageRegistry(
        context.roboto_service_base_url,
        context.http,
    )
    parts = args.remote_image.split(":")
    if len(parts) == 1:
        repository_uri = parts[0]
    elif len(parts) == 2:
        repository_uri, _ = parts
    else:
        raise ValueError("Invalid image format. Expected '<repository>:<tag>'.")

    credentials = image_registry.get_temporary_credentials(
        repository_uri, Permissions.ReadOnly, org_id=args.org
    )
    login_cmd = f"docker login --username {credentials.username} --password-stdin {credentials.registry_url}"
    try:
        subprocess.run(
            shlex.split(login_cmd),
            check=True,
            input=credentials.password,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(
            "Failed to set Docker credentials for Roboto's image registry.",
            file=sys.stderr,
        )
        print(exc.stdout, file=sys.stderr)
        return

    pull_cmd = f"docker pull {args.remote_image}"
    with subprocess.Popen(
        shlex.split(pull_cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as docker_pull_subprocess:
        if not docker_pull_subprocess.stdout:
            raise RuntimeError("Could not start docker pull")

        while docker_pull_subprocess.stdout.readable():
            line = docker_pull_subprocess.stdout.readline()
            if not line:
                break
            print(line, end="")


def pull_parser(parser: argparse.ArgumentParser) -> None:
    add_org_arg(parser)

    parser.add_argument(
        "remote_image",
        action="store",
        help="Specify the remote image to pull, in the format '<repository>:<tag>'.",
    )


pull_command = RobotoCommand(
    name="pull",
    logic=pull,
    setup_parser=pull_parser,
    command_kwargs={
        "help": (
            "Pull a container image hosted in Roboto's image registry. "
            "Requires Docker CLI."
        )
    },
)
