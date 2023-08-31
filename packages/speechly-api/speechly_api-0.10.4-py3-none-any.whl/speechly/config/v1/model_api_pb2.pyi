from speechly.config.v1 import model_pb2 as _model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DownloadModelRequest(_message.Message):
    __slots__ = ["app_id", "config_id", "model_architecture"]
    class ModelArchitecture(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        MODEL_ARCHITECTURE_INVALID: _ClassVar[DownloadModelRequest.ModelArchitecture]
        MODEL_ARCHITECTURE_ORT: _ClassVar[DownloadModelRequest.ModelArchitecture]
        MODEL_ARCHITECTURE_COREML: _ClassVar[DownloadModelRequest.ModelArchitecture]
        MODEL_ARCHITECTURE_TFLITE: _ClassVar[DownloadModelRequest.ModelArchitecture]
    MODEL_ARCHITECTURE_INVALID: DownloadModelRequest.ModelArchitecture
    MODEL_ARCHITECTURE_ORT: DownloadModelRequest.ModelArchitecture
    MODEL_ARCHITECTURE_COREML: DownloadModelRequest.ModelArchitecture
    MODEL_ARCHITECTURE_TFLITE: DownloadModelRequest.ModelArchitecture
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ARCHITECTURE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    config_id: str
    model_architecture: DownloadModelRequest.ModelArchitecture
    def __init__(self, app_id: _Optional[str] = ..., config_id: _Optional[str] = ..., model_architecture: _Optional[_Union[DownloadModelRequest.ModelArchitecture, str]] = ...) -> None: ...

class DownloadModelResponse(_message.Message):
    __slots__ = ["chunk"]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    def __init__(self, chunk: _Optional[bytes] = ...) -> None: ...

class ListBaseModelsRequest(_message.Message):
    __slots__ = ["project_id", "language"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    language: str
    def __init__(self, project_id: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class ListBaseModelsResponse(_message.Message):
    __slots__ = ["model"]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: _containers.RepeatedCompositeFieldContainer[_model_pb2.BaseModel]
    def __init__(self, model: _Optional[_Iterable[_Union[_model_pb2.BaseModel, _Mapping]]] = ...) -> None: ...

class ListLanguagesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListLanguagesResponse(_message.Message):
    __slots__ = ["languages"]
    class Language(_message.Message):
        __slots__ = ["code", "name"]
        CODE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        code: str
        name: str
        def __init__(self, code: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    languages: _containers.RepeatedCompositeFieldContainer[ListLanguagesResponse.Language]
    def __init__(self, languages: _Optional[_Iterable[_Union[ListLanguagesResponse.Language, _Mapping]]] = ...) -> None: ...
