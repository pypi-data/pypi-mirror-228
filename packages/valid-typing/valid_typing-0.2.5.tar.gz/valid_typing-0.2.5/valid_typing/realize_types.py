import typing
from copy import copy

from valid_typing.check_type import check_type

TYPE_MAPPING = {
    list: typing.List,
    set: typing.Set,
    dict: typing.Dict,
}


def set_types(mapping, return_hint):
    if return_hint in mapping:
        return mapping[return_hint]

    if hasattr(return_hint, "__origin__"):
        try:
            return_hint = TYPE_MAPPING[return_hint.__origin__][
                typing.get_args(return_hint)
            ]
        except KeyError:
            pass

        new_args = [set_types(mapping, arg) for arg in return_hint.__args__]
        return_hint = return_hint.__class__(origin=return_hint.__origin__, params=None)
        return_hint.__args__ = new_args

    return return_hint


def generate_mapping(actual, definition, mapping=None):
    if mapping is None:
        mapping = {}

    if isinstance(definition, typing.TypeVar):
        mapping[definition] = actual

    if hasattr(actual, "__origin__") and hasattr(definition, "__origin__"):
        if len(actual.__args__) == len(definition.__args__):
            for i in range(len(actual.__args__)):
                mapping = generate_mapping(
                    actual.__args__[i], definition.__args__[i], mapping=mapping
                )
        else:
            for i in range(len(definition.__args__)):
                mapping = generate_mapping(
                    actual, definition.__args__[i], mapping=mapping
                )
    return mapping


def realize_types(actual, definition, return_hint):
    assert check_type(actual, definition)

    mapping = generate_mapping(actual, definition)

    return set_types(mapping, return_hint)
