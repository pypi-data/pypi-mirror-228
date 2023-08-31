from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiscourseContext(_message.Message):
    __slots__ = ["channel_id", "speaker_id", "listener_ids", "start_time", "end_time"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_ID_FIELD_NUMBER: _ClassVar[int]
    LISTENER_IDS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    speaker_id: str
    listener_ids: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, channel_id: _Optional[str] = ..., speaker_id: _Optional[str] = ..., listener_ids: _Optional[_Iterable[str]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ModerationLabel(_message.Message):
    __slots__ = ["label", "score", "flagged"]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    FLAGGED_FIELD_NUMBER: _ClassVar[int]
    label: str
    score: float
    flagged: bool
    def __init__(self, label: _Optional[str] = ..., score: _Optional[float] = ..., flagged: bool = ...) -> None: ...

class AudioModerationConfig(_message.Message):
    __slots__ = ["model_id", "language_code", "discourse_context"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    DISCOURSE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    language_code: str
    discourse_context: DiscourseContext
    def __init__(self, model_id: _Optional[str] = ..., language_code: _Optional[str] = ..., discourse_context: _Optional[_Union[DiscourseContext, _Mapping]] = ...) -> None: ...

class ModerationSegment(_message.Message):
    __slots__ = ["index", "transcript", "labels", "start_ms", "end_ms"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    START_MS_FIELD_NUMBER: _ClassVar[int]
    END_MS_FIELD_NUMBER: _ClassVar[int]
    index: int
    transcript: str
    labels: _containers.RepeatedCompositeFieldContainer[ModerationLabel]
    start_ms: int
    end_ms: int
    def __init__(self, index: _Optional[int] = ..., transcript: _Optional[str] = ..., labels: _Optional[_Iterable[_Union[ModerationLabel, _Mapping]]] = ..., start_ms: _Optional[int] = ..., end_ms: _Optional[int] = ...) -> None: ...
