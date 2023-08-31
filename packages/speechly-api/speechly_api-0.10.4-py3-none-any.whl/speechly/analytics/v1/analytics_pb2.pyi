from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Aggregation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    AGGREGATION_INVALID: _ClassVar[Aggregation]
    AGGREGATION_MONTHLY: _ClassVar[Aggregation]
    AGGREGATION_DAILY: _ClassVar[Aggregation]
    AGGREGATION_HOURLY: _ClassVar[Aggregation]

class ProcessingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    PROCESSING_TYPE_INVALID: _ClassVar[ProcessingType]
    PROCESSING_TYPE_TRANSCRIPTION: _ClassVar[ProcessingType]
    PROCESSING_TYPE_NLU: _ClassVar[ProcessingType]
    PROCESSING_TYPE_LANGUAGE_DETECTION: _ClassVar[ProcessingType]
    PROCESSING_TYPE_VAD: _ClassVar[ProcessingType]
    PROCESSING_TYPE_TRANSLATION: _ClassVar[ProcessingType]
    PROCESSING_TYPE_AUDIO_EVENT_DETECTION: _ClassVar[ProcessingType]
    PROCESSING_TYPE_TONE_OF_VOICE_LABELLING: _ClassVar[ProcessingType]
    PROCESSING_TYPE_SHALLOW_FUSION: _ClassVar[ProcessingType]
AGGREGATION_INVALID: Aggregation
AGGREGATION_MONTHLY: Aggregation
AGGREGATION_DAILY: Aggregation
AGGREGATION_HOURLY: Aggregation
PROCESSING_TYPE_INVALID: ProcessingType
PROCESSING_TYPE_TRANSCRIPTION: ProcessingType
PROCESSING_TYPE_NLU: ProcessingType
PROCESSING_TYPE_LANGUAGE_DETECTION: ProcessingType
PROCESSING_TYPE_VAD: ProcessingType
PROCESSING_TYPE_TRANSLATION: ProcessingType
PROCESSING_TYPE_AUDIO_EVENT_DETECTION: ProcessingType
PROCESSING_TYPE_TONE_OF_VOICE_LABELLING: ProcessingType
PROCESSING_TYPE_SHALLOW_FUSION: ProcessingType

class UtteranceStatisticsPeriod(_message.Message):
    __slots__ = ["app_id", "start_time", "count", "utterances_seconds", "annotated_seconds", "project_id", "model_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UTTERANCES_SECONDS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    start_time: str
    count: int
    utterances_seconds: int
    annotated_seconds: int
    project_id: str
    model_id: str
    def __init__(self, app_id: _Optional[str] = ..., start_time: _Optional[str] = ..., count: _Optional[int] = ..., utterances_seconds: _Optional[int] = ..., annotated_seconds: _Optional[int] = ..., project_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class Utterance(_message.Message):
    __slots__ = ["transcript", "annotated", "date"]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATED_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    transcript: str
    annotated: str
    date: str
    def __init__(self, transcript: _Optional[str] = ..., annotated: _Optional[str] = ..., date: _Optional[str] = ...) -> None: ...

class DecoderInfo(_message.Message):
    __slots__ = ["version", "utterance_count", "total_seconds_transcribed"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    UTTERANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SECONDS_TRANSCRIBED_FIELD_NUMBER: _ClassVar[int]
    version: str
    utterance_count: int
    total_seconds_transcribed: int
    def __init__(self, version: _Optional[str] = ..., utterance_count: _Optional[int] = ..., total_seconds_transcribed: _Optional[int] = ...) -> None: ...

class ProcessingInfo(_message.Message):
    __slots__ = ["processing_types", "model_id"]
    PROCESSING_TYPES_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    processing_types: _containers.RepeatedScalarFieldContainer[ProcessingType]
    model_id: str
    def __init__(self, processing_types: _Optional[_Iterable[_Union[ProcessingType, str]]] = ..., model_id: _Optional[str] = ...) -> None: ...

class ModerationStatisticsPeriod(_message.Message):
    __slots__ = ["start_time", "user_id", "count", "flagged", "not_flagged", "decisions"]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FLAGGED_FIELD_NUMBER: _ClassVar[int]
    NOT_FLAGGED_FIELD_NUMBER: _ClassVar[int]
    DECISIONS_FIELD_NUMBER: _ClassVar[int]
    start_time: str
    user_id: str
    count: int
    flagged: int
    not_flagged: int
    decisions: int
    def __init__(self, start_time: _Optional[str] = ..., user_id: _Optional[str] = ..., count: _Optional[int] = ..., flagged: _Optional[int] = ..., not_flagged: _Optional[int] = ..., decisions: _Optional[int] = ...) -> None: ...

class UserStatisticsPeriod(_message.Message):
    __slots__ = ["start_time", "active_users", "toxic_users", "exposed_users"]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_USERS_FIELD_NUMBER: _ClassVar[int]
    TOXIC_USERS_FIELD_NUMBER: _ClassVar[int]
    EXPOSED_USERS_FIELD_NUMBER: _ClassVar[int]
    start_time: str
    active_users: int
    toxic_users: int
    exposed_users: int
    def __init__(self, start_time: _Optional[str] = ..., active_users: _Optional[int] = ..., toxic_users: _Optional[int] = ..., exposed_users: _Optional[int] = ...) -> None: ...
