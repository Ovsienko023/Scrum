from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MessageCreateUser:
    name: str
    password: str


@dataclass
class MessageCreatedUser:
    id: UUID
    created_at: datetime

    @property
    def _id(self) -> str:
        return str(self.id)

    @property
    def _created_at(self) -> int:
        return round(self.created_at.timestamp())

    def get_entity(self) -> dict:
        return {
            "id": self._id,
            "created_at": self.created_at,
        }
