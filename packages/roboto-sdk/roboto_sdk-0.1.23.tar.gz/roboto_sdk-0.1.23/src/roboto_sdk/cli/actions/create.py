#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import sys

from ...domain.actions import Action
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import (
    ParseError,
    add_compute_requirements_args,
    add_container_parameters_args,
    add_org_arg,
    parse_compute_requirements,
    parse_container_overrides,
)
from ..context import CLIContext


def create(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    try:
        compute_requirements = parse_compute_requirements(args)
        container_parameters = parse_container_overrides(args)
    except ParseError as exc:
        print(exc.msg, file=sys.stderr)
    else:
        action = Action.create(
            name=args.name,
            action_delegate=context.actions,
            invocation_delegate=context.invocations,
            description=args.description,
            uri=args.image,
            org_id=args.org,
            metadata=args.metadata,
            tags=args.tag,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )

        print(f"Successfully created action '{action.name}'. Record: ")
        print(json.dumps(action.to_dict(), indent=4))


def create_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=True,
        action="store",
        help=(
            "Name of the action. Not modifiable after creation. "
            "An action is considered unique by its (name, docker_image_name, docker_image_tag) tuple."
        ),
    )
    parser.add_argument(
        "--description",
        required=False,
        action="store",
        help="Optional description of action. Modifiable after creation.",
    )
    parser.add_argument(
        "--image",
        required=False,
        action="store",
        dest="image",
        help="Register a Docker image with this action. Modifiable after creation.",
    )
    parser.add_argument(
        "--metadata",
        required=False,
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key=value' format key/value pairs which represent action metadata. "
            "`value` is parsed as JSON. "
            "Metadata can be modified after creation."
        ),
    )
    parser.add_argument(
        "--tag",
        required=False,
        type=str,
        nargs="*",
        help="One or more tags to annotate this action. Modifiable after creation.",
        action="extend",
    )
    add_org_arg(parser=parser)

    add_compute_requirements_args(parser)
    add_container_parameters_args(parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_parser,
    command_kwargs={"help": "Create a new action."},
)
