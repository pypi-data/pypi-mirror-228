import collections.abc
import decimal
import enum
import json
import typing

import pydantic

from .serde import safe_dict_drill


class Comparator(str, enum.Enum):
    """The comparator to use when comparing a field to a value."""

    Equals = "EQUALS"
    NotEquals = "NOT_EQUALS"
    GreaterThan = "GREATER_THAN"
    GreaterThanOrEqual = "GREATER_THAN_OR_EQUAL"
    LessThan = "LESS_THAN"
    LessThanOrEqual = "LESS_THAN_OR_EQUAL"
    Contains = "CONTAINS"
    NotContains = "NOT_CONTAINS"
    IsNull = "IS_NULL"
    IsNotNull = "IS_NOT_NULL"
    Exists = "EXISTS"
    NotExists = "NOT_EXISTS"
    BeginsWith = "BEGINS_WITH"


class Condition(pydantic.BaseModel):
    """A filter for any arbitrary attribute for a Roboto resource."""

    field: str
    comparator: Comparator
    value: typing.Optional[typing.Union[str, bool, int, float, decimal.Decimal]] = None

    @pydantic.validator("value")
    def parse(cls, v):
        if v is None:
            return None
        try:
            return json.loads(v)
        except json.decoder.JSONDecodeError:
            return v

    def matches(self, target: dict) -> bool:
        value = safe_dict_drill(target, self.field.split("."))

        if self.comparator in [Comparator.NotExists, Comparator.IsNull]:
            return value is None

        if self.comparator in [Comparator.Exists, Comparator.IsNotNull]:
            return value is not None

        # We need the value for everything else
        if value is None:
            return False

        if self.comparator is Comparator.Equals:
            return value == self.value

        if self.comparator is Comparator.NotEquals:
            return value != self.value

        if self.comparator is Comparator.GreaterThan:
            return value > self.value

        if self.comparator is Comparator.GreaterThanOrEqual:
            return value >= self.value

        if self.comparator is Comparator.LessThan:
            return value < self.value

        if self.comparator is Comparator.LessThanOrEqual:
            return value <= self.value

        if self.comparator is Comparator.Contains:
            return isinstance(value, list) and self.value in value

        if self.comparator is Comparator.NotContains:
            return isinstance(value, list) and self.value not in value

        if self.comparator is Comparator.BeginsWith:
            if not isinstance(value, str) or not isinstance(self.value, str):
                return False

            return value.startswith(self.value)

        return False


class ConditionOperator(str, enum.Enum):
    """The operator to use when combining multiple conditions."""

    And = "AND"
    Or = "OR"
    Not = "NOT"


class ConditionGroup(pydantic.BaseModel):
    """A group of conditions that are combined together."""

    operator: ConditionOperator
    conditions: collections.abc.Sequence[typing.Union[Condition, "ConditionGroup"]]

    def matches(self, target: dict):
        inner_matches = map(lambda x: x.matches(target), self.conditions)

        if self.operator is ConditionOperator.And:
            return all(inner_matches)

        if self.operator is ConditionOperator.Or:
            return any(inner_matches)

        if self.operator is ConditionOperator.Not:
            return not any(inner_matches)

        return False


ConditionType = typing.Union[Condition, ConditionGroup]


class SortDirection(str, enum.Enum):
    """The direction to sort the results of a query."""

    Ascending = "ASC"
    Descending = "DESC"


class QuerySpecification(pydantic.BaseModel):
    """
    Model for specifying a query to the Roboto Platform.

    Examples:
        Specify a query with a single condition:
            >>> from roboto_sdk import query
            >>> query_spec = query.QuerySpecification(
            ...     condition=query.Condition(
            ...         field="name",
            ...         comparator=query.Comparator.Equals,
            ...         value="Roboto"
            ...     )
            ... )

        Specify a query with multiple conditions:
            >>> from roboto_sdk import query
            >>> query_spec = query.QuerySpecification(
            ...     condition=query.ConditionGroup(
            ...         operator=query.ConditionOperator.And,
            ...         conditions=[
            ...             query.Condition(
            ...                 field="name",
            ...                 comparator=query.Comparator.Equals,
            ...                 value="Roboto"
            ...             ),
            ...             query.Condition(
            ...                 field="age",
            ...                 comparator=query.Comparator.GreaterThan,
            ...                 value=18
            ...             )
            ...         ]
            ...     )
            ... )

        Arbitrarily nest condition groups:
            >>> from roboto_sdk import query
            >>> query_spec = query.QuerySpecification(
            ...     condition=query.ConditionGroup(
            ...         operator=query.ConditionOperator.And,
            ...         conditions=[
            ...             query.Condition(
            ...                 field="name",
            ...                 comparator=query.Comparator.Equals,
            ...                 value="Roboto"
            ...             ),
            ...             query.ConditionGroup(
            ...                 operator=query.ConditionOperator.Or,
            ...                 conditions=[
            ...                     query.Condition(
            ...                         field="age",
            ...                         comparator=query.Comparator.GreaterThan,
            ...                         value=18
            ...                     ),
            ...                     query.Condition(
            ...                         field="age",
            ...                         comparator=query.Comparator.LessThan,
            ...                         value=30
            ...                     )
            ...                 ]
            ...             )
            ...         ]
            ...     )
            ... )
    """

    condition: typing.Optional[typing.Union[Condition, ConditionGroup]] = None
    limit: int = 1000
    after: typing.Optional[str] = None  # An encoded PaginationToken
    sort_by: typing.Optional[str] = None
    sort_direction: typing.Optional[SortDirection] = None

    class Config:
        extra = "forbid"

    @classmethod
    def protected_from_oldstyle_request(
        cls, filters: dict, page_token: typing.Optional[str] = None
    ) -> "QuerySpecification":
        """
        Convert deprecated query format to new format.

        Not for public use.

        :meta private:
        """
        conditions: list[typing.Union[Condition, ConditionGroup]] = []

        def _iterconditions(field: str, value: typing.Any):
            if isinstance(value, list):
                conditions.append(
                    ConditionGroup(
                        operator=ConditionOperator.Or,
                        conditions=[
                            Condition(
                                field=field, comparator=Comparator.Equals, value=v
                            )
                            for v in value
                        ],
                    )
                )

            elif isinstance(value, dict):
                for k, v in value.items():
                    _iterconditions(f"{field}.{k}", v)

            else:
                conditions.append(
                    Condition(field=field, comparator=Comparator.Equals, value=value)
                )

        for field, value in filters.items():
            _iterconditions(field, value)

        return cls(
            condition=ConditionGroup(
                operator=ConditionOperator.And, conditions=conditions
            ),
            after=page_token,
        )

    def fields(self) -> set[str]:
        """Return a set of all fields referenced in the query."""
        fields = set()

        def _iterconditions(
            condition: typing.Optional[typing.Union[Condition, ConditionGroup]]
        ):
            if condition is None:
                return

            if isinstance(condition, Condition):
                fields.add(condition.field)
            else:
                for cond in condition.conditions:
                    _iterconditions(cond)

        _iterconditions(self.condition)
        return fields
