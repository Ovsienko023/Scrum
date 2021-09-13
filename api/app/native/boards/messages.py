from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MessageCreateBoard:
    title: str


@dataclass
class MessageCreatedBoard:
    board_id: UUID
    created_at: datetime
