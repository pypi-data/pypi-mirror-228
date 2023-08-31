from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationScope(_message.Message):
    __slots__ = ["app_id", "config_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    config_id: str
    def __init__(self, app_id: _Optional[str] = ..., config_id: _Optional[str] = ...) -> None: ...

class ProjectScope(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...
