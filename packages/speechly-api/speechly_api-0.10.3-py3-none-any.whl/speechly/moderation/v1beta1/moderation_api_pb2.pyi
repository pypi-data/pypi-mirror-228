from speechly.moderation.v1beta1 import moderation_pb2 as _moderation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TextModerationRequest(_message.Message):
    __slots__ = ["model_id", "text", "discourse_context", "language_code", "audio_context_id"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    DISCOURSE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    text: str
    discourse_context: _moderation_pb2.DiscourseContext
    language_code: str
    audio_context_id: str
    def __init__(self, model_id: _Optional[str] = ..., text: _Optional[str] = ..., discourse_context: _Optional[_Union[_moderation_pb2.DiscourseContext, _Mapping]] = ..., language_code: _Optional[str] = ..., audio_context_id: _Optional[str] = ...) -> None: ...

class TextModerationResponse(_message.Message):
    __slots__ = ["labels"]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[_moderation_pb2.ModerationLabel]
    def __init__(self, labels: _Optional[_Iterable[_Union[_moderation_pb2.ModerationLabel, _Mapping]]] = ...) -> None: ...

class AudioModerationRequest(_message.Message):
    __slots__ = ["config", "audio"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    config: _moderation_pb2.AudioModerationConfig
    audio: bytes
    def __init__(self, config: _Optional[_Union[_moderation_pb2.AudioModerationConfig, _Mapping]] = ..., audio: _Optional[bytes] = ...) -> None: ...

class AudioModerationResponse(_message.Message):
    __slots__ = ["segments"]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[_moderation_pb2.ModerationSegment]
    def __init__(self, segments: _Optional[_Iterable[_Union[_moderation_pb2.ModerationSegment, _Mapping]]] = ...) -> None: ...

class StreamingAudioModerationRequest(_message.Message):
    __slots__ = ["config", "audio"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    config: _moderation_pb2.AudioModerationConfig
    audio: bytes
    def __init__(self, config: _Optional[_Union[_moderation_pb2.AudioModerationConfig, _Mapping]] = ..., audio: _Optional[bytes] = ...) -> None: ...

class StreamingAudioModerationResponse(_message.Message):
    __slots__ = ["segment"]
    SEGMENT_FIELD_NUMBER: _ClassVar[int]
    segment: _moderation_pb2.ModerationSegment
    def __init__(self, segment: _Optional[_Union[_moderation_pb2.ModerationSegment, _Mapping]] = ...) -> None: ...
