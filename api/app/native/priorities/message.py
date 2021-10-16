from typing import List
from dataclasses import dataclass


@dataclass
class MessagePriority:
    title: str


@dataclass
class MessagePriorities:
    count: int
    priorities: List[MessagePriority]
