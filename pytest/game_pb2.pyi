from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BallType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Normal: _ClassVar[BallType]
    Wide: _ClassVar[BallType]
    NoBall: _ClassVar[BallType]
    Wicket: _ClassVar[BallType]
Normal: BallType
Wide: BallType
NoBall: BallType
Wicket: BallType

class BallEvent(_message.Message):
    __slots__ = ("type", "ballerName", "batsmenName", "runsScored")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BALLERNAME_FIELD_NUMBER: _ClassVar[int]
    BATSMENNAME_FIELD_NUMBER: _ClassVar[int]
    RUNSSCORED_FIELD_NUMBER: _ClassVar[int]
    type: BallType
    ballerName: str
    batsmenName: str
    runsScored: int
    def __init__(self, type: _Optional[_Union[BallType, str]] = ..., ballerName: _Optional[str] = ..., batsmenName: _Optional[str] = ..., runsScored: _Optional[int] = ...) -> None: ...

class InningsData(_message.Message):
    __slots__ = ("score", "wickets", "balls")
    SCORE_FIELD_NUMBER: _ClassVar[int]
    WICKETS_FIELD_NUMBER: _ClassVar[int]
    BALLS_FIELD_NUMBER: _ClassVar[int]
    score: int
    wickets: int
    balls: int
    def __init__(self, score: _Optional[int] = ..., wickets: _Optional[int] = ..., balls: _Optional[int] = ...) -> None: ...

class Game(_message.Message):
    __slots__ = ("gameId", "player1", "player2", "firstPlayerInnings", "firstInnings", "secondInnings", "balls", "gameOver", "winner")
    GAMEID_FIELD_NUMBER: _ClassVar[int]
    PLAYER1_FIELD_NUMBER: _ClassVar[int]
    PLAYER2_FIELD_NUMBER: _ClassVar[int]
    FIRSTPLAYERINNINGS_FIELD_NUMBER: _ClassVar[int]
    FIRSTINNINGS_FIELD_NUMBER: _ClassVar[int]
    SECONDINNINGS_FIELD_NUMBER: _ClassVar[int]
    BALLS_FIELD_NUMBER: _ClassVar[int]
    GAMEOVER_FIELD_NUMBER: _ClassVar[int]
    WINNER_FIELD_NUMBER: _ClassVar[int]
    gameId: str
    player1: str
    player2: str
    firstPlayerInnings: bool
    firstInnings: InningsData
    secondInnings: InningsData
    balls: _containers.RepeatedCompositeFieldContainer[BallEvent]
    gameOver: bool
    winner: str
    def __init__(self, gameId: _Optional[str] = ..., player1: _Optional[str] = ..., player2: _Optional[str] = ..., firstPlayerInnings: bool = ..., firstInnings: _Optional[_Union[InningsData, _Mapping]] = ..., secondInnings: _Optional[_Union[InningsData, _Mapping]] = ..., balls: _Optional[_Iterable[_Union[BallEvent, _Mapping]]] = ..., gameOver: bool = ..., winner: _Optional[str] = ...) -> None: ...

class CreateGameRequest(_message.Message):
    __slots__ = ("player1", "player2")
    PLAYER1_FIELD_NUMBER: _ClassVar[int]
    PLAYER2_FIELD_NUMBER: _ClassVar[int]
    player1: str
    player2: str
    def __init__(self, player1: _Optional[str] = ..., player2: _Optional[str] = ...) -> None: ...

class CreateGameResponse(_message.Message):
    __slots__ = ("game",)
    GAME_FIELD_NUMBER: _ClassVar[int]
    game: Game
    def __init__(self, game: _Optional[_Union[Game, _Mapping]] = ...) -> None: ...

class GetGameRequest(_message.Message):
    __slots__ = ("gameId",)
    GAMEID_FIELD_NUMBER: _ClassVar[int]
    gameId: str
    def __init__(self, gameId: _Optional[str] = ...) -> None: ...
