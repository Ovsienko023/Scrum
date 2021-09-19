from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.native.estimation import EstimationTime

@dataclass
class MessageGetCard:
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

    def __post_init__(self):
        self.estimates_time = EstimationTime(hours=self.estimates_time)


@dataclass
class MessageCreateCard:
    title: str
    description: str
    developer_id: UUID
    priority_id: UUID
    status_id: UUID
    board_id: UUID
    creator_id: UUID
    estimation: int


@dataclass
class MessageCreatedCard:
    card_id: int
    created_at: datetime
