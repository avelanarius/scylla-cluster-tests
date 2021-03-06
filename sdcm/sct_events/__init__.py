# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2020 ScyllaDB

import enum
import json
import logging
from typing import Protocol, Optional, Type, runtime_checkable


class Severity(enum.Enum):
    UNKNOWN = 0
    NORMAL = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@runtime_checkable
class SctEventProtocol(Protocol):
    base: str
    type: Optional[str]
    subtype: Optional[str]
    timestamp: Optional[float]
    severity: Severity

    def __init__(self, *args, **kwargs):
        ...

    @classmethod
    def is_abstract(cls) -> bool:
        ...

    @classmethod
    def add_subevent_type(cls,
                          name: str,
                          /, *,
                          abstract: bool = False,
                          mixin: Optional[Type] = None,
                          **kwargs) -> None:
        ...

    @property
    def formatted_timestamp(self) -> str:
        ...

    def publish(self) -> None:
        ...

    def publish_or_dump(self, default_logger: Optional[logging.Logger] = None) -> None:
        ...

    def to_json(self) -> str:
        ...


# Monkey patch JSONEncoder make enums jsonable
_SAVED_DEFAULT = json.JSONEncoder().default  # save default method.


def _new_default(self, obj):  # pylint: disable=unused-argument
    if isinstance(obj, enum.Enum):
        return obj.name  # could also be obj.value
    else:
        return _SAVED_DEFAULT


json.JSONEncoder.default = _new_default  # set new default method.


__all__ = ("SctEventProtocol", "Severity", )
