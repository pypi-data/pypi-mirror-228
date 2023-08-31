from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class App(_message.Message):
    __slots__ = ["app_id", "name", "language", "current_config_id", "current_model_url", "current_plan", "status", "current_ort_model_url", "current_coreml_model_url", "current_tflite_model_url"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        INVALID: _ClassVar[App.Status]
        ACTIVE: _ClassVar[App.Status]
        INACTIVE: _ClassVar[App.Status]
        DELETED: _ClassVar[App.Status]
    INVALID: App.Status
    ACTIVE: App.Status
    INACTIVE: App.Status
    DELETED: App.Status
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MODEL_URL_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PLAN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ORT_MODEL_URL_FIELD_NUMBER: _ClassVar[int]
    CURRENT_COREML_MODEL_URL_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TFLITE_MODEL_URL_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    name: str
    language: str
    current_config_id: str
    current_model_url: str
    current_plan: str
    status: App.Status
    current_ort_model_url: str
    current_coreml_model_url: str
    current_tflite_model_url: str
    def __init__(self, app_id: _Optional[str] = ..., name: _Optional[str] = ..., language: _Optional[str] = ..., current_config_id: _Optional[str] = ..., current_model_url: _Optional[str] = ..., current_plan: _Optional[str] = ..., status: _Optional[_Union[App.Status, str]] = ..., current_ort_model_url: _Optional[str] = ..., current_coreml_model_url: _Optional[str] = ..., current_tflite_model_url: _Optional[str] = ...) -> None: ...

class Project(_message.Message):
    __slots__ = ["project_id", "name", "selected_plan"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SELECTED_PLAN_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    name: str
    selected_plan: PaymentPlan
    def __init__(self, project_id: _Optional[str] = ..., name: _Optional[str] = ..., selected_plan: _Optional[_Union[PaymentPlan, _Mapping]] = ...) -> None: ...

class Participant(_message.Message):
    __slots__ = ["subject_id", "name", "email", "type", "created_by"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        USER: _ClassVar[Participant.Type]
        TOKEN: _ClassVar[Participant.Type]
    USER: Participant.Type
    TOKEN: Participant.Type
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    subject_id: str
    name: str
    email: str
    type: Participant.Type
    created_by: Participant
    def __init__(self, subject_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., type: _Optional[_Union[Participant.Type, str]] = ..., created_by: _Optional[_Union[Participant, _Mapping]] = ...) -> None: ...

class PaymentPlan(_message.Message):
    __slots__ = ["id", "alias", "name", "description", "monthly_credits", "start_date", "end_date"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_CREDITS_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    alias: str
    name: str
    description: str
    monthly_credits: int
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., alias: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., monthly_credits: _Optional[int] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListProjectsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListProjectsResponse(_message.Message):
    __slots__ = ["projects"]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    projects: _containers.RepeatedCompositeFieldContainer[Project]
    def __init__(self, projects: _Optional[_Iterable[_Union[Project, _Mapping]]] = ...) -> None: ...

class ListAppsRequest(_message.Message):
    __slots__ = ["project_id", "list_all_apps"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    LIST_ALL_APPS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    list_all_apps: bool
    def __init__(self, project_id: _Optional[str] = ..., list_all_apps: bool = ...) -> None: ...

class ListAppsResponse(_message.Message):
    __slots__ = ["project_id", "apps"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    APPS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    apps: _containers.RepeatedCompositeFieldContainer[App]
    def __init__(self, project_id: _Optional[str] = ..., apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ...) -> None: ...

class FindAppRequest(_message.Message):
    __slots__ = ["app_id", "config_id", "when_in_use"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    WHEN_IN_USE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    config_id: str
    when_in_use: _timestamp_pb2.Timestamp
    def __init__(self, app_id: _Optional[str] = ..., config_id: _Optional[str] = ..., when_in_use: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FindAppResponse(_message.Message):
    __slots__ = ["app"]
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class ProjectExistsRequest(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ProjectExistsResponse(_message.Message):
    __slots__ = ["exists"]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    exists: bool
    def __init__(self, exists: bool = ...) -> None: ...

class CreateProjectRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateProjectResponse(_message.Message):
    __slots__ = ["project"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: Project
    def __init__(self, project: _Optional[_Union[Project, _Mapping]] = ...) -> None: ...

class GetProjectRequest(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetProjectResponse(_message.Message):
    __slots__ = ["project"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: Project
    def __init__(self, project: _Optional[_Union[Project, _Mapping]] = ...) -> None: ...

class UpdateProjectRequest(_message.Message):
    __slots__ = ["project_id", "name"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    name: str
    def __init__(self, project_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateProjectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteProjectRequest(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class DeleteProjectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListParticipantsRequest(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class ListParticipantsResponse(_message.Message):
    __slots__ = ["project_id", "participants"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    participants: _containers.RepeatedCompositeFieldContainer[Participant]
    def __init__(self, project_id: _Optional[str] = ..., participants: _Optional[_Iterable[_Union[Participant, _Mapping]]] = ...) -> None: ...

class InviteParticipantRequest(_message.Message):
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class InviteParticipantResponse(_message.Message):
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
    __slots__ = ["project_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class RemoveParticipantRequest(_message.Message):
    __slots__ = ["project_id", "subject_id"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    subject_id: str
    def __init__(self, project_id: _Optional[str] = ..., subject_id: _Optional[str] = ...) -> None: ...

class RemoveParticipantResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListPaymentPlansRequest(_message.Message):
    __slots__ = ["active_date"]
    ACTIVE_DATE_FIELD_NUMBER: _ClassVar[int]
    active_date: _timestamp_pb2.Timestamp
    def __init__(self, active_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListPaymentPlansResponse(_message.Message):
    __slots__ = ["plans"]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[PaymentPlan]
    def __init__(self, plans: _Optional[_Iterable[_Union[PaymentPlan, _Mapping]]] = ...) -> None: ...

class SelectPaymentPlanRequest(_message.Message):
    __slots__ = ["project_id", "plan_id", "plan_alias", "start_date"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ALIAS_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    plan_id: str
    plan_alias: str
    start_date: _timestamp_pb2.Timestamp
    def __init__(self, project_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., plan_alias: _Optional[str] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SelectPaymentPlanResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
