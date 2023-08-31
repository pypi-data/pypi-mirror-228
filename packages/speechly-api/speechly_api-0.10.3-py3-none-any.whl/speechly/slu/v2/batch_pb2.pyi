from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatchTasks(_message.Message):
    __slots__ = ["transcribe", "translate"]
    TRANSCRIBE_FIELD_NUMBER: _ClassVar[int]
    TRANSLATE_FIELD_NUMBER: _ClassVar[int]
    transcribe: bool
    translate: bool
    def __init__(self, transcribe: bool = ..., translate: bool = ...) -> None: ...

class BatchOutput(_message.Message):
    __slots__ = ["display", "lexical", "tokenized"]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    LEXICAL_FIELD_NUMBER: _ClassVar[int]
    TOKENIZED_FIELD_NUMBER: _ClassVar[int]
    display: bool
    lexical: bool
    tokenized: bool
    def __init__(self, display: bool = ..., lexical: bool = ..., tokenized: bool = ...) -> None: ...

class BatchConfig(_message.Message):
    __slots__ = ["model_id", "language_codes", "batch_reference", "priority", "options"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODES_FIELD_NUMBER: _ClassVar[int]
    BATCH_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    language_codes: _containers.RepeatedScalarFieldContainer[str]
    batch_reference: str
    priority: int
    options: _containers.RepeatedCompositeFieldContainer[Option]
    def __init__(self, model_id: _Optional[str] = ..., language_codes: _Optional[_Iterable[str]] = ..., batch_reference: _Optional[str] = ..., priority: _Optional[int] = ..., options: _Optional[_Iterable[_Union[Option, _Mapping]]] = ...) -> None: ...

class ProcessAudioSourceRequestItem(_message.Message):
    __slots__ = ["source_url", "destination_url", "completion_webhook", "reference", "device_id"]
    SOURCE_URL_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_URL_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    source_url: str
    destination_url: str
    completion_webhook: HttpResource
    reference: str
    device_id: str
    def __init__(self, source_url: _Optional[str] = ..., destination_url: _Optional[str] = ..., completion_webhook: _Optional[_Union[HttpResource, _Mapping]] = ..., reference: _Optional[str] = ..., device_id: _Optional[str] = ...) -> None: ...

class Operation(_message.Message):
    __slots__ = ["id", "reference", "batch_id", "batch_reference", "status", "language_code", "app_id", "result", "duration", "error_code", "error_description", "source_url", "destination_url"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        STATUS_UNSPECIFIED: _ClassVar[Operation.Status]
        STATUS_PENDING: _ClassVar[Operation.Status]
        STATUS_DONE: _ClassVar[Operation.Status]
        STATUS_ERROR: _ClassVar[Operation.Status]
    STATUS_UNSPECIFIED: Operation.Status
    STATUS_PENDING: Operation.Status
    STATUS_DONE: Operation.Status
    STATUS_ERROR: Operation.Status
    class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        ERROR_UNSPECIFIED: _ClassVar[Operation.ErrorCode]
        ERROR_UNSUPPORTED_LANGUAGE: _ClassVar[Operation.ErrorCode]
        ERROR_INTERNAL: _ClassVar[Operation.ErrorCode]
        ERROR_INVALID_PARAMETERS: _ClassVar[Operation.ErrorCode]
        ERROR_INVALID_SOURCE: _ClassVar[Operation.ErrorCode]
        ERROR_INVALID_DESTINATION: _ClassVar[Operation.ErrorCode]
        ERROR_INVALID_AUDIO: _ClassVar[Operation.ErrorCode]
    ERROR_UNSPECIFIED: Operation.ErrorCode
    ERROR_UNSUPPORTED_LANGUAGE: Operation.ErrorCode
    ERROR_INTERNAL: Operation.ErrorCode
    ERROR_INVALID_PARAMETERS: Operation.ErrorCode
    ERROR_INVALID_SOURCE: Operation.ErrorCode
    ERROR_INVALID_DESTINATION: Operation.ErrorCode
    ERROR_INVALID_AUDIO: Operation.ErrorCode
    ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_URL_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    reference: str
    batch_id: str
    batch_reference: str
    status: Operation.Status
    language_code: str
    app_id: str
    result: _containers.RepeatedCompositeFieldContainer[OperationResult]
    duration: _duration_pb2.Duration
    error_code: Operation.ErrorCode
    error_description: str
    source_url: str
    destination_url: str
    def __init__(self, id: _Optional[str] = ..., reference: _Optional[str] = ..., batch_id: _Optional[str] = ..., batch_reference: _Optional[str] = ..., status: _Optional[_Union[Operation.Status, str]] = ..., language_code: _Optional[str] = ..., app_id: _Optional[str] = ..., result: _Optional[_Iterable[_Union[OperationResult, _Mapping]]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., error_code: _Optional[_Union[Operation.ErrorCode, str]] = ..., error_description: _Optional[str] = ..., source_url: _Optional[str] = ..., destination_url: _Optional[str] = ...) -> None: ...

class OperationResult(_message.Message):
    __slots__ = ["type", "text", "tokens"]
    class ResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        RESULT_TYPE_UNSPECIFIED: _ClassVar[OperationResult.ResultType]
        RESULT_TYPE_TRANSCRIPT_LEXICAL: _ClassVar[OperationResult.ResultType]
        RESULT_TYPE_TRANSCRIPT_DISPLAY: _ClassVar[OperationResult.ResultType]
        RESULT_TYPE_TRANSLATION: _ClassVar[OperationResult.ResultType]
    RESULT_TYPE_UNSPECIFIED: OperationResult.ResultType
    RESULT_TYPE_TRANSCRIPT_LEXICAL: OperationResult.ResultType
    RESULT_TYPE_TRANSCRIPT_DISPLAY: OperationResult.ResultType
    RESULT_TYPE_TRANSLATION: OperationResult.ResultType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    type: OperationResult.ResultType
    text: str
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    def __init__(self, type: _Optional[_Union[OperationResult.ResultType, str]] = ..., text: _Optional[str] = ..., tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ["token", "index", "start_time", "end_time"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    token: str
    index: int
    start_time: int
    end_time: int
    def __init__(self, token: _Optional[str] = ..., index: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class Option(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Iterable[str]] = ...) -> None: ...

class HttpResource(_message.Message):
    __slots__ = ["url", "method", "headers"]
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        METHOD_UNSPECIFIED: _ClassVar[HttpResource.Method]
        METHOD_GET: _ClassVar[HttpResource.Method]
        METHOD_POST: _ClassVar[HttpResource.Method]
        METHOD_PUT: _ClassVar[HttpResource.Method]
    METHOD_UNSPECIFIED: HttpResource.Method
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
