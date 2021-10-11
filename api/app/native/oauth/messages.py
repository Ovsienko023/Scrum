from uuid import UUID
from dataclasses import dataclass


@dataclass
class MessageGetToken:
    login: str
    password: str


@dataclass
class MessageToken:
    access_token: UUID
