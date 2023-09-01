from __future__ import annotations

from typing_extensions import TypeAlias
from typing import Callable

from kelvin.sdk.datatype import KRN, KMessageTypeData, Message

KelvinFilterType: TypeAlias = Callable[[Message], bool]


def is_data_message(msg: Message) -> bool:
    return msg.type.msg_type == "data"


def is_parameter(msg: Message) -> bool:
    return msg.type.msg_type == "parameter"


def is_configuration(msg: Message) -> bool:
    # todo: implement after define how configuration changes are received
    return False


def resource_equal(resource: KRN) -> KelvinFilterType:
    return lambda msg: msg.resource == resource
