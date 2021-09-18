from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


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
    estimates_time: int
    board_id: UUID
    creator_id: UUID
    created_at: datetime


@dataclass
class MessageCreateCard:
    title: str
    description: str
    developer_id: UUID
    priority_id: UUID
    status_id: UUID
    board_id: UUID
    creator_id: UUID
    estimates_time: int


@dataclass
class MessageCreatedCard:
    card_id: int
    created_at: datetime
