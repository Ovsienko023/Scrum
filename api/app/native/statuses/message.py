from uuid import UUID
from typing import List
from dataclasses import dataclass


@dataclass
class MessageStatus:
    status_id: UUID
    title: str


@dataclass
class MessageStatuses:
    count: int
    statuses: List[MessageStatus]
