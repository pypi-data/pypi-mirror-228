#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import shlex
import subprocess

from ...auth import Permissions
from ...image_registry import ImageRegistry
from ...waiters import TimeoutError, wait_for
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def push(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    image_registry = ImageRegistry(
        context.roboto_service_base_url,
        context.http,
    )
    parts = args.local_image.split(":")
    if len(parts) == 1:
        repo, tag = parts[0], "latest"
    elif len(parts) == 2:
        repo, tag = parts
    else:
        raise ValueError("Invalid image format. Expected '<repository>:<tag>'.")
    repository = image_registry.create_repository(repo, org_id=args.org)
    credentials = image_registry.get_temporary_credentials(
        repository["repository_uri"], Permissions.ReadWrite, org_id=args.org
    )
    cmd = f"docker login --username {credentials.username} --password-stdin {credentials.registry_url}"
    subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        check=True,
        input=credentials.password,
        text=True,
    )

    image_uri = f"{repository['repository_uri']}:{tag}"
    cmd = f"docker tag {args.local_image} {image_uri}"
    subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        check=True,
        text=True,
    )
    cmd = f"docker push {image_uri}"
    with subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as docker_push_subprocess:
        if not docker_push_subprocess.stdout:
            raise RuntimeError("Could not start docker push")

        while docker_push_subprocess.stdout.readable():
            line = docker_push_subprocess.stdout.readline()
            if not line:
                break
            print(line, end="")

    print("Waiting for image to be available...")
    try:
        wait_for(
            image_registry.repository_contains_image,
            args=[repository["repository_name"], tag, args.org],
            interval=lambda iteration: min((2**iteration) / 2, 32),
        )
        print(
            f"Image pushed successfully! You can now use '{image_uri}' in your Roboto Actions."
        )
    except TimeoutError:
        print(
            "Image could not be confirmed as successfully pushed. Try pushing again in a few minutes."
        )
    except KeyboardInterrupt:
        print("")


def push_parser(parser: argparse.ArgumentParser) -> None:
    add_org_arg(parser)

    parser.add_argument(
        "local_image",
        action="store",
        help="Specify the local image to push, in the format '<repository>:<tag>'.",
    )


push_command = RobotoCommand(
    name="push",
    logic=push,
    setup_parser=push_parser,
    command_kwargs={
        "help": (
            "Push a local container image into Roboto's image registry."
            "Requires Docker CLI."
        )
    },
)
