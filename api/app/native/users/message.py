from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MessageCreateUser:
    name: str
    password: str


@dataclass
class MessageCreatedUser:
    user_id: UUID
    created_at: datetime
