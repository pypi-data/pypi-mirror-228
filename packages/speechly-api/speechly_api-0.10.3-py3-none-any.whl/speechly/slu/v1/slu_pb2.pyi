from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SLURequest(_message.Message):
    __slots__ = ["config", "event", "audio", "rtt_response", "start", "stop"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    RTT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    config: SLUConfig
    event: SLUEvent
    audio: bytes
    rtt_response: RoundTripMeasurementResponse
    start: SLUStart
    stop: SLUStop
    def __init__(self, config: _Optional[_Union[SLUConfig, _Mapping]] = ..., event: _Optional[_Union[SLUEvent, _Mapping]] = ..., audio: _Optional[bytes] = ..., rtt_response: _Optional[_Union[RoundTripMeasurementResponse, _Mapping]] = ..., start: _Optional[_Union[SLUStart, _Mapping]] = ..., stop: _Optional[_Union[SLUStop, _Mapping]] = ...) -> None: ...

class SLUConfig(_message.Message):
    __slots__ = ["encoding", "channels", "sample_rate_hertz", "language_code", "options"]
    class Encoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        LINEAR16: _ClassVar[SLUConfig.Encoding]
    LINEAR16: SLUConfig.Encoding
    class Option(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Iterable[str]] = ...) -> None: ...
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_HERTZ_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    encoding: SLUConfig.Encoding
    channels: int
    sample_rate_hertz: int
    language_code: str
    options: _containers.RepeatedCompositeFieldContainer[SLUConfig.Option]
    def __init__(self, encoding: _Optional[_Union[SLUConfig.Encoding, str]] = ..., channels: _Optional[int] = ..., sample_rate_hertz: _Optional[int] = ..., language_code: _Optional[str] = ..., options: _Optional[_Iterable[_Union[SLUConfig.Option, _Mapping]]] = ...) -> None: ...

class SLUEvent(_message.Message):
    __slots__ = ["event", "app_id"]
    class Event(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        START: _ClassVar[SLUEvent.Event]
        STOP: _ClassVar[SLUEvent.Event]
    START: SLUEvent.Event
    STOP: SLUEvent.Event
    EVENT_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    event: SLUEvent.Event
    app_id: str
    def __init__(self, event: _Optional[_Union[SLUEvent.Event, str]] = ..., app_id: _Optional[str] = ...) -> None: ...

class SLUStart(_message.Message):
    __slots__ = ["app_id", "options"]
    class Option(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Iterable[str]] = ...) -> None: ...
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    options: _containers.RepeatedCompositeFieldContainer[SLUStart.Option]
    def __init__(self, app_id: _Optional[str] = ..., options: _Optional[_Iterable[_Union[SLUStart.Option, _Mapping]]] = ...) -> None: ...

class SLUStop(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SLUResponse(_message.Message):
    __slots__ = ["audio_context", "segment_id", "transcript", "entity", "intent", "segment_end", "tentative_transcript", "tentative_entities", "tentative_intent", "started", "finished", "rtt_request"]
    AUDIO_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_END_FIELD_NUMBER: _ClassVar[int]
    TENTATIVE_TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    TENTATIVE_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    TENTATIVE_INTENT_FIELD_NUMBER: _ClassVar[int]
    STARTED_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    RTT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    audio_context: str
    segment_id: int
    transcript: SLUTranscript
    entity: SLUEntity
    intent: SLUIntent
    segment_end: SLUSegmentEnd
    tentative_transcript: SLUTentativeTranscript
    tentative_entities: SLUTentativeEntities
    tentative_intent: SLUIntent
    started: SLUStarted
    finished: SLUFinished
    rtt_request: RoundTripMeasurementRequest
    def __init__(self, audio_context: _Optional[str] = ..., segment_id: _Optional[int] = ..., transcript: _Optional[_Union[SLUTranscript, _Mapping]] = ..., entity: _Optional[_Union[SLUEntity, _Mapping]] = ..., intent: _Optional[_Union[SLUIntent, _Mapping]] = ..., segment_end: _Optional[_Union[SLUSegmentEnd, _Mapping]] = ..., tentative_transcript: _Optional[_Union[SLUTentativeTranscript, _Mapping]] = ..., tentative_entities: _Optional[_Union[SLUTentativeEntities, _Mapping]] = ..., tentative_intent: _Optional[_Union[SLUIntent, _Mapping]] = ..., started: _Optional[_Union[SLUStarted, _Mapping]] = ..., finished: _Optional[_Union[SLUFinished, _Mapping]] = ..., rtt_request: _Optional[_Union[RoundTripMeasurementRequest, _Mapping]] = ...) -> None: ...

class SLUTranscript(_message.Message):
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

class SLUEntity(_message.Message):
    __slots__ = ["entity", "value", "start_position", "end_position"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    START_POSITION_FIELD_NUMBER: _ClassVar[int]
    END_POSITION_FIELD_NUMBER: _ClassVar[int]
    entity: str
    value: str
    start_position: int
    end_position: int
    def __init__(self, entity: _Optional[str] = ..., value: _Optional[str] = ..., start_position: _Optional[int] = ..., end_position: _Optional[int] = ...) -> None: ...

class SLUIntent(_message.Message):
    __slots__ = ["intent"]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    intent: str
    def __init__(self, intent: _Optional[str] = ...) -> None: ...

class SLUSegmentEnd(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SLUTentativeTranscript(_message.Message):
    __slots__ = ["tentative_transcript", "tentative_words"]
    TENTATIVE_TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    TENTATIVE_WORDS_FIELD_NUMBER: _ClassVar[int]
    tentative_transcript: str
    tentative_words: _containers.RepeatedCompositeFieldContainer[SLUTranscript]
    def __init__(self, tentative_transcript: _Optional[str] = ..., tentative_words: _Optional[_Iterable[_Union[SLUTranscript, _Mapping]]] = ...) -> None: ...

class SLUTentativeEntities(_message.Message):
    __slots__ = ["tentative_entities"]
    TENTATIVE_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    tentative_entities: _containers.RepeatedCompositeFieldContainer[SLUEntity]
    def __init__(self, tentative_entities: _Optional[_Iterable[_Union[SLUEntity, _Mapping]]] = ...) -> None: ...

class SLUStarted(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SLUFinished(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: SLUError
    def __init__(self, error: _Optional[_Union[SLUError, _Mapping]] = ...) -> None: ...

class SLUError(_message.Message):
    __slots__ = ["code", "message"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class RoundTripMeasurementRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RoundTripMeasurementResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
