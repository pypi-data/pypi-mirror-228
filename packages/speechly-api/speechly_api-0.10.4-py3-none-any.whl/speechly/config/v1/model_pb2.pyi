from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BaseModel(_message.Message):
    __slots__ = ["name", "alias", "is_downloadable", "is_streamable", "language"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    IS_DOWNLOADABLE_FIELD_NUMBER: _ClassVar[int]
    IS_STREAMABLE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    alias: str
    is_downloadable: bool
    is_streamable: bool
    language: str
    def __init__(self, name: _Optional[str] = ..., alias: _Optional[str] = ..., is_downloadable: bool = ..., is_streamable: bool = ..., language: _Optional[str] = ...) -> None: ...
