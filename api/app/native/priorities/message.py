from uuid import UUID
from typing import List
from dataclasses import dataclass


@dataclass
class MessagePriority:
    priority_id: UUID
    title: str


@dataclass
class MessagePriorities:
    count: int
    priorities: List[MessagePriority]
