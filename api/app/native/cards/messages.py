from dataclasses import dataclass
from datetime import datetime
from typing import Any, List
from uuid import UUID

from app.native.estimation import EstimationTime


@dataclass
class MessageGetCard:
    creator_id: UUID
    card_id: int


@dataclass
class MessageCard:
    card_id: int
    title: str
    description: str
    developer_id: UUID
    priority: str
    status: str
    estimates_time: Any
    board_id: UUID
    creator_id: UUID
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self.estimates_time = EstimationTime(hours=self.estimates_time)


@dataclass
class MessageCreateCard:
    title: str
    description: str
    developer_id: UUID
    priority: str
    board_id: UUID
    creator_id: UUID
    estimation: str


@dataclass
class MessageCreatedCard:
    card_id: int
    created_at: datetime


@dataclass
class MessageUpdateCard:
    card_id: int
    title: str
    description: str
    developer_id: UUID
    priority_id: UUID
    status_id: UUID
    board_id: UUID
    estimation: Any

    def __post_init__(self):
        self.estimation = EstimationTime().convert_to_hours(times=self.estimation)


@dataclass
class MessageGetReport:
    board_id: UUID
    status_id: UUID
    priority_id: UUID
    developer_id: UUID


@dataclass
class MessageReported:
    estimation: str or None
    cards: List[MessageCard]


@dataclass
class MessageRemoveCard:
    card_id: int
