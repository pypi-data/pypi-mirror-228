from speechly.identity.v2 import identity_pb2 as _identity_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ["device_id", "application", "project"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    application: _identity_pb2.ApplicationScope
    project: _identity_pb2.ProjectScope
    def __init__(self, device_id: _Optional[str] = ..., application: _Optional[_Union[_identity_pb2.ApplicationScope, _Mapping]] = ..., project: _Optional[_Union[_identity_pb2.ProjectScope, _Mapping]] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ["token", "valid_for_s", "expires_at_epoch", "expires_at"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    VALID_FOR_S_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_EPOCH_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    token: str
    valid_for_s: int
    expires_at_epoch: int
    expires_at: str
    def __init__(self, token: _Optional[str] = ..., valid_for_s: _Optional[int] = ..., expires_at_epoch: _Optional[int] = ..., expires_at: _Optional[str] = ...) -> None: ...
