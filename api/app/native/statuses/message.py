from typing import List
from dataclasses import dataclass


@dataclass
class MessageStatus:
    title: str


@dataclass
class MessageStatuses:
    count: int
    statuses: List[MessageStatus]
