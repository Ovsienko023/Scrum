from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MessageGetBoard:
    board_id: int


@dataclass
class MessageBoard:
    board_id: UUID
    title: str
    creator_id: UUID
    created_at: datetime


@dataclass
class MessageCreateBoard:
    title: str


@dataclass
class MessageCreatedBoard:
    board_id: UUID
    created_at: datetime
