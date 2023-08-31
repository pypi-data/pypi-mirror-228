from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AppSource(_message.Message):
    __slots__ = ["app_id", "language", "data_chunk", "content_type"]
    class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CONTENT_TYPE_UNSPECIFIED: _ClassVar[AppSource.ContentType]
        CONTENT_TYPE_YAML: _ClassVar[AppSource.ContentType]
        CONTENT_TYPE_TAR: _ClassVar[AppSource.ContentType]
    CONTENT_TYPE_UNSPECIFIED: AppSource.ContentType
    CONTENT_TYPE_YAML: AppSource.ContentType
    CONTENT_TYPE_TAR: AppSource.ContentType
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    language: str
    data_chunk: bytes
    content_type: AppSource.ContentType
    def __init__(self, app_id: _Optional[str] = ..., language: _Optional[str] = ..., data_chunk: _Optional[bytes] = ..., content_type: _Optional[_Union[AppSource.ContentType, str]] = ...) -> None: ...

class CompileRequest(_message.Message):
    __slots__ = ["app_source", "batch_size", "random_seed"]
    APP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    RANDOM_SEED_FIELD_NUMBER: _ClassVar[int]
    app_source: AppSource
    batch_size: int
    random_seed: int
    def __init__(self, app_source: _Optional[_Union[AppSource, _Mapping]] = ..., batch_size: _Optional[int] = ..., random_seed: _Optional[int] = ...) -> None: ...

class CompileResult(_message.Message):
    __slots__ = ["result", "templates", "messages"]
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        COMPILE_SUCCESS: _ClassVar[CompileResult.Result]
        COMPILE_FAILURE: _ClassVar[CompileResult.Result]
        COMPILE_WARNING: _ClassVar[CompileResult.Result]
    COMPILE_SUCCESS: CompileResult.Result
    COMPILE_FAILURE: CompileResult.Result
    COMPILE_WARNING: CompileResult.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    result: CompileResult.Result
    templates: _containers.RepeatedScalarFieldContainer[str]
    messages: _containers.RepeatedCompositeFieldContainer[LineReference]
    def __init__(self, result: _Optional[_Union[CompileResult.Result, str]] = ..., templates: _Optional[_Iterable[str]] = ..., messages: _Optional[_Iterable[_Union[LineReference, _Mapping]]] = ...) -> None: ...

class ConvertRequest(_message.Message):
    __slots__ = ["input_format", "language", "data_chunk"]
    class InputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        FORMAT_UNKNOWN: _ClassVar[ConvertRequest.InputFormat]
        FORMAT_ALEXA: _ClassVar[ConvertRequest.InputFormat]
    FORMAT_UNKNOWN: ConvertRequest.InputFormat
    FORMAT_ALEXA: ConvertRequest.InputFormat
    INPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    input_format: ConvertRequest.InputFormat
    language: str
    data_chunk: bytes
    def __init__(self, input_format: _Optional[_Union[ConvertRequest.InputFormat, str]] = ..., language: _Optional[str] = ..., data_chunk: _Optional[bytes] = ...) -> None: ...

class ConvertResult(_message.Message):
    __slots__ = ["status", "warnings", "result"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CONVERT_SUCCESS: _ClassVar[ConvertResult.Status]
        CONVERT_WARNINGS: _ClassVar[ConvertResult.Status]
        CONVERT_FAILED: _ClassVar[ConvertResult.Status]
    CONVERT_SUCCESS: ConvertResult.Status
    CONVERT_WARNINGS: ConvertResult.Status
    CONVERT_FAILED: ConvertResult.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    status: ConvertResult.Status
    warnings: str
    result: AppSource
    def __init__(self, status: _Optional[_Union[ConvertResult.Status, str]] = ..., warnings: _Optional[str] = ..., result: _Optional[_Union[AppSource, _Mapping]] = ...) -> None: ...

class ValidateResult(_message.Message):
    __slots__ = ["messages"]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[LineReference]
    def __init__(self, messages: _Optional[_Iterable[_Union[LineReference, _Mapping]]] = ...) -> None: ...

class LineReference(_message.Message):
    __slots__ = ["line", "column", "file", "level", "message"]
    class Level(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        LEVEL_NOTE: _ClassVar[LineReference.Level]
        LEVEL_WARNING: _ClassVar[LineReference.Level]
        LEVEL_ERROR: _ClassVar[LineReference.Level]
    LEVEL_NOTE: LineReference.Level
    LEVEL_WARNING: LineReference.Level
    LEVEL_ERROR: LineReference.Level
    LINE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    line: int
    column: int
    file: str
    level: LineReference.Level
    message: str
    def __init__(self, line: _Optional[int] = ..., column: _Optional[int] = ..., file: _Optional[str] = ..., level: _Optional[_Union[LineReference.Level, str]] = ..., message: _Optional[str] = ...) -> None: ...

class ExtractSALSourcesResult(_message.Message):
    __slots__ = ["data_chunk"]
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    data_chunk: bytes
    def __init__(self, data_chunk: _Optional[bytes] = ...) -> None: ...
