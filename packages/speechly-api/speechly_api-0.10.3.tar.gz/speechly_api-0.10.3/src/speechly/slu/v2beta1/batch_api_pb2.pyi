from speechly.slu.v2beta1 import batch_pb2 as _batch_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessAudioSourceRequest(_message.Message):
    __slots__ = ["config", "source"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    config: _batch_pb2.ProcessAudioBatchConfig
    source: _containers.RepeatedCompositeFieldContainer[_batch_pb2.ProcessAudioSourceRequestItem]
    def __init__(self, config: _Optional[_Union[_batch_pb2.ProcessAudioBatchConfig, _Mapping]] = ..., source: _Optional[_Iterable[_Union[_batch_pb2.ProcessAudioSourceRequestItem, _Mapping]]] = ...) -> None: ...

class ProcessAudioSourceResponse(_message.Message):
    __slots__ = ["operation"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    operation: _containers.RepeatedCompositeFieldContainer[_batch_pb2.Operation]
    def __init__(self, operation: _Optional[_Iterable[_Union[_batch_pb2.Operation, _Mapping]]] = ...) -> None: ...

class QueryStatusRequest(_message.Message):
    __slots__ = ["operation_ids", "operation_references", "batch_id", "batch_reference"]
    OPERATION_IDS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    operation_ids: _containers.RepeatedScalarFieldContainer[str]
    operation_references: _containers.RepeatedScalarFieldContainer[str]
    batch_id: str
    batch_reference: str
    def __init__(self, operation_ids: _Optional[_Iterable[str]] = ..., operation_references: _Optional[_Iterable[str]] = ..., batch_id: _Optional[str] = ..., batch_reference: _Optional[str] = ...) -> None: ...

class QueryStatusResponse(_message.Message):
    __slots__ = ["operation"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    operation: _containers.RepeatedCompositeFieldContainer[_batch_pb2.Operation]
    def __init__(self, operation: _Optional[_Iterable[_Union[_batch_pb2.Operation, _Mapping]]] = ...) -> None: ...
