#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import typing

from ...domain.actions import Action
from ...query import (
    Comparator,
    Condition,
    ConditionGroup,
    ConditionOperator,
    QuerySpecification,
)
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import add_org_arg
from ..context import CLIContext


def search(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    conditions: list[typing.Union[Condition, ConditionGroup]] = []
    if args.name:
        conditions.append(
            Condition(
                field="name",
                comparator=Comparator.Equals,
                value=args.name,
            )
        )

    if args.metadata:
        for key, value in args.metadata.items():
            conditions.append(
                Condition(
                    field=f"metadata.{key}",
                    comparator=Comparator.Equals,
                    value=value,
                )
            )

    if args.tag:
        for tag in args.tag:
            conditions.append(
                Condition(
                    field="tags",
                    comparator=Comparator.Contains,
                    value=tag,
                )
            )

    query = QuerySpecification(
        condition=ConditionGroup(
            conditions=conditions,
            operator=ConditionOperator.And,
        )
    )

    matching_actions = Action.query(
        query,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    print(json.dumps([action.to_dict() for action in matching_actions], indent=4))


def search_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=False,
        action="store",
        help="If querying by action name, must provide an exact match; patterns are not accepted.",
    )
    parser.add_argument(
        "--metadata",
        required=False,
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key=value' pairs which represent action metadata. "
            "`value` is parsed as JSON. E.g.: --metadata foo=bar --metadata baz.nested=200"
        ),
    )
    parser.add_argument(
        "--tag",
        required=False,
        type=str,
        nargs="*",
        help="One or more tags associated with this action. E.g.: --tag foo --tag bar",
        action="extend",
    )
    add_org_arg(parser=parser)


search_command = RobotoCommand(
    name="search",
    logic=search,
    setup_parser=search_parser,
    command_kwargs={"help": "Search for existing actions."},
)
