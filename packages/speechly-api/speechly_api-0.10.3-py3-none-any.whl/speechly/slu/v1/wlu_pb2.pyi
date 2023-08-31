from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TextsRequest(_message.Message):
    __slots__ = ["app_id", "requests"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    requests: _containers.RepeatedCompositeFieldContainer[WLURequest]
    def __init__(self, app_id: _Optional[str] = ..., requests: _Optional[_Iterable[_Union[WLURequest, _Mapping]]] = ...) -> None: ...

class TextsResponse(_message.Message):
    __slots__ = ["responses"]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[WLUResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[WLUResponse, _Mapping]]] = ...) -> None: ...

class WLURequest(_message.Message):
    __slots__ = ["language_code", "text", "reference_time"]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_TIME_FIELD_NUMBER: _ClassVar[int]
    language_code: str
    text: str
    reference_time: _timestamp_pb2.Timestamp
    def __init__(self, language_code: _Optional[str] = ..., text: _Optional[str] = ..., reference_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class WLUResponse(_message.Message):
    __slots__ = ["segments"]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[WLUSegment]
    def __init__(self, segments: _Optional[_Iterable[_Union[WLUSegment, _Mapping]]] = ...) -> None: ...

class WLUSegment(_message.Message):
    __slots__ = ["text", "tokens", "entities", "intent", "annotated_text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATED_TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    tokens: _containers.RepeatedCompositeFieldContainer[WLUToken]
    entities: _containers.RepeatedCompositeFieldContainer[WLUEntity]
    intent: WLUIntent
    annotated_text: str
    def __init__(self, text: _Optional[str] = ..., tokens: _Optional[_Iterable[_Union[WLUToken, _Mapping]]] = ..., entities: _Optional[_Iterable[_Union[WLUEntity, _Mapping]]] = ..., intent: _Optional[_Union[WLUIntent, _Mapping]] = ..., annotated_text: _Optional[str] = ...) -> None: ...

class WLUToken(_message.Message):
    __slots__ = ["word", "index"]
    WORD_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    word: str
    index: int
    def __init__(self, word: _Optional[str] = ..., index: _Optional[int] = ...) -> None: ...

class WLUEntity(_message.Message):
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

class WLUIntent(_message.Message):
    __slots__ = ["intent"]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    intent: str
    def __init__(self, intent: _Optional[str] = ...) -> None: ...
