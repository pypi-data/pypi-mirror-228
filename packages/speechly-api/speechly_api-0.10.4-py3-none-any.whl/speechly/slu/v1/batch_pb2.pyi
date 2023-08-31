from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioConfiguration(_message.Message):
    __slots__ = ["encoding", "channels", "sample_rate_hertz", "language_codes"]
    class Encoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        ENCODING_INVALID: _ClassVar[AudioConfiguration.Encoding]
        ENCODING_LINEAR16: _ClassVar[AudioConfiguration.Encoding]
    ENCODING_INVALID: AudioConfiguration.Encoding
    ENCODING_LINEAR16: AudioConfiguration.Encoding
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_HERTZ_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODES_FIELD_NUMBER: _ClassVar[int]
    encoding: AudioConfiguration.Encoding
    channels: int
    sample_rate_hertz: int
    language_codes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, encoding: _Optional[_Union[AudioConfiguration.Encoding, str]] = ..., channels: _Optional[int] = ..., sample_rate_hertz: _Optional[int] = ..., language_codes: _Optional[_Iterable[str]] = ...) -> None: ...

class HttpResource(_message.Message):
    __slots__ = ["url", "method", "headers"]
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        METHOD_INVALID: _ClassVar[HttpResource.Method]
        METHOD_GET: _ClassVar[HttpResource.Method]
        METHOD_POST: _ClassVar[HttpResource.Method]
        METHOD_PUT: _ClassVar[HttpResource.Method]
    METHOD_INVALID: HttpResource.Method
    METHOD_GET: HttpResource.Method
    METHOD_POST: HttpResource.Method
    METHOD_PUT: HttpResource.Method
    class Header(_message.Message):
        __slots__ = ["name", "value"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    URL_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    url: str
    method: HttpResource.Method
    headers: _containers.RepeatedCompositeFieldContainer[HttpResource.Header]
    def __init__(self, url: _Optional[str] = ..., method: _Optional[_Union[HttpResource.Method, str]] = ..., headers: _Optional[_Iterable[_Union[HttpResource.Header, _Mapping]]] = ...) -> None: ...

class Operation(_message.Message):
    __slots__ = ["id", "reference", "status", "language_code", "app_id", "device_id", "transcripts", "error", "duration"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        STATUS_INVALID: _ClassVar[Operation.Status]
        STATUS_QUEUED: _ClassVar[Operation.Status]
        STATUS_PROCESSING: _ClassVar[Operation.Status]
        STATUS_DONE: _ClassVar[Operation.Status]
        STATUS_ERROR: _ClassVar[Operation.Status]
        STATUS_ANALYSING: _ClassVar[Operation.Status]
        STATUS_WAITING_DECODER: _ClassVar[Operation.Status]
    STATUS_INVALID: Operation.Status
    STATUS_QUEUED: Operation.Status
    STATUS_PROCESSING: Operation.Status
    STATUS_DONE: Operation.Status
    STATUS_ERROR: Operation.Status
    STATUS_ANALYSING: Operation.Status
    STATUS_WAITING_DECODER: Operation.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    reference: str
    status: Operation.Status
    language_code: str
    app_id: str
    device_id: str
    transcripts: _containers.RepeatedCompositeFieldContainer[Transcript]
    error: str
    duration: _duration_pb2.Duration
    def __init__(self, id: _Optional[str] = ..., reference: _Optional[str] = ..., status: _Optional[_Union[Operation.Status, str]] = ..., language_code: _Optional[str] = ..., app_id: _Optional[str] = ..., device_id: _Optional[str] = ..., transcripts: _Optional[_Iterable[_Union[Transcript, _Mapping]]] = ..., error: _Optional[str] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class Transcript(_message.Message):
    __slots__ = ["word", "index", "start_time", "end_time"]
    WORD_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    word: str
    index: int
    start_time: int
    end_time: int
    def __init__(self, word: _Optional[str] = ..., index: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class Option(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Iterable[str]] = ...) -> None: ...
