from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MessageCreateUser:
    display_name: str
    login: str
    password: str


@dataclass
class MessageCreatedUser:
    user_id: UUID
    created_at: datetime
