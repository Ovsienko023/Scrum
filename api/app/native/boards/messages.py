from uuid import UUID
from typing import List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MessageGetBoard:
    board_id: UUID


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


@dataclass
class MessageUpdateBoard:
    board_id: UUID
    title: str


@dataclass
class MessageBoards:
    count: int
    boards: List[MessageBoard]


@dataclass
class MessageRemoveBoard:
    board_id: UUID
