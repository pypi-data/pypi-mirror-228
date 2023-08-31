from speechly.slu.v1 import batch_pb2 as _batch_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessAudioRequest(_message.Message):
    __slots__ = ["app_id", "device_id", "config", "audio", "uri", "http_source", "results_uri", "http_result", "reference", "options"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    HTTP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_URI_FIELD_NUMBER: _ClassVar[int]
    HTTP_RESULT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    device_id: str
    config: _batch_pb2.AudioConfiguration
    audio: bytes
    uri: str
    http_source: _batch_pb2.HttpResource
    results_uri: str
    http_result: _batch_pb2.HttpResource
    reference: str
    options: _containers.RepeatedCompositeFieldContainer[_batch_pb2.Option]
    def __init__(self, app_id: _Optional[str] = ..., device_id: _Optional[str] = ..., config: _Optional[_Union[_batch_pb2.AudioConfiguration, _Mapping]] = ..., audio: _Optional[bytes] = ..., uri: _Optional[str] = ..., http_source: _Optional[_Union[_batch_pb2.HttpResource, _Mapping]] = ..., results_uri: _Optional[str] = ..., http_result: _Optional[_Union[_batch_pb2.HttpResource, _Mapping]] = ..., reference: _Optional[str] = ..., options: _Optional[_Iterable[_Union[_batch_pb2.Option, _Mapping]]] = ...) -> None: ...

class ProcessAudioResponse(_message.Message):
    __slots__ = ["operation"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    operation: _batch_pb2.Operation
    def __init__(self, operation: _Optional[_Union[_batch_pb2.Operation, _Mapping]] = ...) -> None: ...

class QueryStatusRequest(_message.Message):
    __slots__ = ["id", "reference"]
    ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    reference: str
    def __init__(self, id: _Optional[str] = ..., reference: _Optional[str] = ...) -> None: ...

class QueryStatusResponse(_message.Message):
    __slots__ = ["operation"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    operation: _batch_pb2.Operation
    def __init__(self, operation: _Optional[_Union[_batch_pb2.Operation, _Mapping]] = ...) -> None: ...
