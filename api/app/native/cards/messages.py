from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


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
