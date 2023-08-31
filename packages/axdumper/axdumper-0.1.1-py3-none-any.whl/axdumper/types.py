from typing import runtime_checkable, Protocol


__all__ = [
    'DictConvertAble',
    'StringifyAble',
]


@runtime_checkable
class DictConvertAble(Protocol):
    def to_dict(self):
        raise NotImplemented


@runtime_checkable
class StringifyAble(Protocol):
    def stringify(self):
        raise NotImplemented

