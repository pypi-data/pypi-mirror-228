from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProjectRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetProjectResponse(_message.Message):
    __slots__ = ["project", "project_names"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAMES_FIELD_NUMBER: _ClassVar[int]
    project: _containers.RepeatedScalarFieldContainer[str]
    project_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project: _Optional[_Iterable[str]] = ..., project_names: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateProjectRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateProjectResponse(_message.Message):
    __slots__ = ["project", "name"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    project: str
    name: str
    def __init__(self, project: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateProjectRequest(_message.Message):
    __slots__ = ["project", "name"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    project: str
    name: str
    def __init__(self, project: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateProjectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetProjectParticipantsRequest(_message.Message):
    __slots__ = ["project"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: str
    def __init__(self, project: _Optional[str] = ...) -> None: ...

class GetProjectParticipantsResponse(_message.Message):
    __slots__ = ["participants"]
    class Participant(_message.Message):
        __slots__ = ["name", "email", "id"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        name: str
        email: str
        id: str
        def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    participants: _containers.RepeatedCompositeFieldContainer[GetProjectParticipantsResponse.Participant]
    def __init__(self, participants: _Optional[_Iterable[_Union[GetProjectParticipantsResponse.Participant, _Mapping]]] = ...) -> None: ...

class InviteRequest(_message.Message):
    __slots__ = ["project"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: str
    def __init__(self, project: _Optional[str] = ...) -> None: ...

class InviteResponse(_message.Message):
    __slots__ = ["invitation_token"]
    INVITATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    invitation_token: str
    def __init__(self, invitation_token: _Optional[str] = ...) -> None: ...

class JoinProjectRequest(_message.Message):
    __slots__ = ["invitation_token"]
    INVITATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    invitation_token: str
    def __init__(self, invitation_token: _Optional[str] = ...) -> None: ...

class JoinProjectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListAppsRequest(_message.Message):
    __slots__ = ["project"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: str
    def __init__(self, project: _Optional[str] = ...) -> None: ...

class ListAppsResponse(_message.Message):
    __slots__ = ["apps"]
    APPS_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[App]
    def __init__(self, apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ...) -> None: ...

class GetAppRequest(_message.Message):
    __slots__ = ["app_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class GetAppResponse(_message.Message):
    __slots__ = ["app"]
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class CreateAppRequest(_message.Message):
    __slots__ = ["project", "app"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    project: str
    app: App
    def __init__(self, project: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class CreateAppResponse(_message.Message):
    __slots__ = ["app"]
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class UpdateAppRequest(_message.Message):
    __slots__ = ["app"]
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class UpdateAppResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteAppRequest(_message.Message):
    __slots__ = ["app_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class DeleteAppResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UploadTrainingDataRequest(_message.Message):
    __slots__ = ["app_id", "data_chunk", "content_type"]
    class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CONTENT_TYPE_UNSPECIFIED: _ClassVar[UploadTrainingDataRequest.ContentType]
        CONTENT_TYPE_YAML: _ClassVar[UploadTrainingDataRequest.ContentType]
        CONTENT_TYPE_TAR: _ClassVar[UploadTrainingDataRequest.ContentType]
    CONTENT_TYPE_UNSPECIFIED: UploadTrainingDataRequest.ContentType
    CONTENT_TYPE_YAML: UploadTrainingDataRequest.ContentType
    CONTENT_TYPE_TAR: UploadTrainingDataRequest.ContentType
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    data_chunk: bytes
    content_type: UploadTrainingDataRequest.ContentType
    def __init__(self, app_id: _Optional[str] = ..., data_chunk: _Optional[bytes] = ..., content_type: _Optional[_Union[UploadTrainingDataRequest.ContentType, str]] = ...) -> None: ...

class UploadTrainingDataResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DownloadCurrentTrainingDataRequest(_message.Message):
    __slots__ = ["app_id", "config_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    config_id: str
    def __init__(self, app_id: _Optional[str] = ..., config_id: _Optional[str] = ...) -> None: ...

class DownloadCurrentTrainingDataResponse(_message.Message):
    __slots__ = ["data_chunk", "content_type"]
    class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CONTENT_TYPE_UNSPECIFIED: _ClassVar[DownloadCurrentTrainingDataResponse.ContentType]
        CONTENT_TYPE_YAML: _ClassVar[DownloadCurrentTrainingDataResponse.ContentType]
        CONTENT_TYPE_TAR: _ClassVar[DownloadCurrentTrainingDataResponse.ContentType]
    CONTENT_TYPE_UNSPECIFIED: DownloadCurrentTrainingDataResponse.ContentType
    CONTENT_TYPE_YAML: DownloadCurrentTrainingDataResponse.ContentType
    CONTENT_TYPE_TAR: DownloadCurrentTrainingDataResponse.ContentType
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    data_chunk: bytes
    content_type: DownloadCurrentTrainingDataResponse.ContentType
    def __init__(self, data_chunk: _Optional[bytes] = ..., content_type: _Optional[_Union[DownloadCurrentTrainingDataResponse.ContentType, str]] = ...) -> None: ...

class App(_message.Message):
    __slots__ = ["id", "language", "status", "name", "queue_size", "error_msg", "estimated_remaining_sec", "estimated_training_time_sec", "training_time_sec", "tags", "deployed_at_time"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        STATUS_UNSPECIFIED: _ClassVar[App.Status]
        STATUS_NEW: _ClassVar[App.Status]
        STATUS_TRAINING: _ClassVar[App.Status]
        STATUS_TRAINED: _ClassVar[App.Status]
        STATUS_FAILED: _ClassVar[App.Status]
        STATUS_INACTIVE: _ClassVar[App.Status]
        STATUS_DELETED: _ClassVar[App.Status]
    STATUS_UNSPECIFIED: App.Status
    STATUS_NEW: App.Status
    STATUS_TRAINING: App.Status
    STATUS_TRAINED: App.Status
    STATUS_FAILED: App.Status
    STATUS_INACTIVE: App.Status
    STATUS_DELETED: App.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_REMAINING_SEC_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_TRAINING_TIME_SEC_FIELD_NUMBER: _ClassVar[int]
    TRAINING_TIME_SEC_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYED_AT_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    language: str
    status: App.Status
    name: str
    queue_size: int
    error_msg: str
    estimated_remaining_sec: int
    estimated_training_time_sec: int
    training_time_sec: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    deployed_at_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., language: _Optional[str] = ..., status: _Optional[_Union[App.Status, str]] = ..., name: _Optional[str] = ..., queue_size: _Optional[int] = ..., error_msg: _Optional[str] = ..., estimated_remaining_sec: _Optional[int] = ..., estimated_training_time_sec: _Optional[int] = ..., training_time_sec: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., deployed_at_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
