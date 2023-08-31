from speechly.analytics.v1 import analytics_pb2 as _analytics_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UtteranceStatisticsRequest(_message.Message):
    __slots__ = ["app_id", "days", "scope", "aggregation", "start_date", "end_date", "project_id"]
    class Scope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        SCOPE_INVALID: _ClassVar[UtteranceStatisticsRequest.Scope]
        SCOPE_UTTERANCES: _ClassVar[UtteranceStatisticsRequest.Scope]
        SCOPE_ANNOTATIONS: _ClassVar[UtteranceStatisticsRequest.Scope]
        SCOPE_ALL: _ClassVar[UtteranceStatisticsRequest.Scope]
    SCOPE_INVALID: UtteranceStatisticsRequest.Scope
    SCOPE_UTTERANCES: UtteranceStatisticsRequest.Scope
    SCOPE_ANNOTATIONS: UtteranceStatisticsRequest.Scope
    SCOPE_ALL: UtteranceStatisticsRequest.Scope
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DAYS_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    days: int
    scope: UtteranceStatisticsRequest.Scope
    aggregation: _analytics_pb2.Aggregation
    start_date: str
    end_date: str
    project_id: str
    def __init__(self, app_id: _Optional[str] = ..., days: _Optional[int] = ..., scope: _Optional[_Union[UtteranceStatisticsRequest.Scope, str]] = ..., aggregation: _Optional[_Union[_analytics_pb2.Aggregation, str]] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class UtteranceStatisticsResponse(_message.Message):
    __slots__ = ["start_date", "end_date", "aggregation", "items", "total_utterances", "total_duration_seconds", "total_annotated_seconds"]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_UTTERANCES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ANNOTATED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    start_date: str
    end_date: str
    aggregation: _analytics_pb2.Aggregation
    items: _containers.RepeatedCompositeFieldContainer[_analytics_pb2.UtteranceStatisticsPeriod]
    total_utterances: int
    total_duration_seconds: int
    total_annotated_seconds: int
    def __init__(self, start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., aggregation: _Optional[_Union[_analytics_pb2.Aggregation, str]] = ..., items: _Optional[_Iterable[_Union[_analytics_pb2.UtteranceStatisticsPeriod, _Mapping]]] = ..., total_utterances: _Optional[int] = ..., total_duration_seconds: _Optional[int] = ..., total_annotated_seconds: _Optional[int] = ...) -> None: ...

class UtterancesRequest(_message.Message):
    __slots__ = ["app_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class UtterancesResponse(_message.Message):
    __slots__ = ["utterances"]
    UTTERANCES_FIELD_NUMBER: _ClassVar[int]
    utterances: _containers.RepeatedCompositeFieldContainer[_analytics_pb2.Utterance]
    def __init__(self, utterances: _Optional[_Iterable[_Union[_analytics_pb2.Utterance, _Mapping]]] = ...) -> None: ...

class RegisterUtteranceRequest(_message.Message):
    __slots__ = ["app_id", "device_id", "utterance_length_seconds", "utterance_length_chars", "decoder_info", "created_time", "finished_time", "status", "operation_id", "batch_id", "project_id", "language", "processing_info"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        STATUS_INVALID: _ClassVar[RegisterUtteranceRequest.Status]
        STATUS_SUCCESS: _ClassVar[RegisterUtteranceRequest.Status]
        STATUS_ERROR: _ClassVar[RegisterUtteranceRequest.Status]
    STATUS_INVALID: RegisterUtteranceRequest.Status
    STATUS_SUCCESS: RegisterUtteranceRequest.Status
    STATUS_ERROR: RegisterUtteranceRequest.Status
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    UTTERANCE_LENGTH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    UTTERANCE_LENGTH_CHARS_FIELD_NUMBER: _ClassVar[int]
    DECODER_INFO_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIME_FIELD_NUMBER: _ClassVar[int]
    FINISHED_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_INFO_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    device_id: str
    utterance_length_seconds: int
    utterance_length_chars: int
    decoder_info: _analytics_pb2.DecoderInfo
    created_time: _timestamp_pb2.Timestamp
    finished_time: _timestamp_pb2.Timestamp
    status: RegisterUtteranceRequest.Status
    operation_id: str
    batch_id: str
    project_id: str
    language: str
    processing_info: _analytics_pb2.ProcessingInfo
    def __init__(self, app_id: _Optional[str] = ..., device_id: _Optional[str] = ..., utterance_length_seconds: _Optional[int] = ..., utterance_length_chars: _Optional[int] = ..., decoder_info: _Optional[_Union[_analytics_pb2.DecoderInfo, _Mapping]] = ..., created_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., finished_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[RegisterUtteranceRequest.Status, str]] = ..., operation_id: _Optional[str] = ..., batch_id: _Optional[str] = ..., project_id: _Optional[str] = ..., language: _Optional[str] = ..., processing_info: _Optional[_Union[_analytics_pb2.ProcessingInfo, _Mapping]] = ...) -> None: ...

class RegisterUtteranceResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RegisterUtterancesRequest(_message.Message):
    __slots__ = ["requests"]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[RegisterUtteranceRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[RegisterUtteranceRequest, _Mapping]]] = ...) -> None: ...

class RegisterUtterancesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ModerationStatisticsRequest(_message.Message):
    __slots__ = ["project_id", "app_id", "start_date", "end_date", "aggregation"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    app_id: str
    start_date: str
    end_date: str
    aggregation: _analytics_pb2.Aggregation
    def __init__(self, project_id: _Optional[str] = ..., app_id: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., aggregation: _Optional[_Union[_analytics_pb2.Aggregation, str]] = ...) -> None: ...

class ModerationStatisticsResponse(_message.Message):
    __slots__ = ["project_id", "app_id", "start_date", "end_date", "aggregation", "items", "total_events", "total_flagged", "total_not_flagged"]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EVENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FLAGGED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_NOT_FLAGGED_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    app_id: str
    start_date: str
    end_date: str
    aggregation: _analytics_pb2.Aggregation
    items: _containers.RepeatedCompositeFieldContainer[_analytics_pb2.ModerationStatisticsPeriod]
    total_events: int
    total_flagged: int
    total_not_flagged: int
    def __init__(self, project_id: _Optional[str] = ..., app_id: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., aggregation: _Optional[_Union[_analytics_pb2.Aggregation, str]] = ..., items: _Optional[_Iterable[_Union[_analytics_pb2.ModerationStatisticsPeriod, _Mapping]]] = ..., total_events: _Optional[int] = ..., total_flagged: _Optional[int] = ..., total_not_flagged: _Optional[int] = ...) -> None: ...

class UserStatisticsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UserStatisticsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
