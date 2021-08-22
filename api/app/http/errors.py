from aiohttp import web
from typing import List


class ErrorContainer:
    def __init__(self,
                 code: int = 200,
                 description: str = None,
                 details: List[dict] = None):
        self._code = code
        self._description = description
        self._details = details or []

    @property
    def code(self) -> int:
        return self._code

    @property
    def description(self) -> str:
        return self._description

    @property
    def details(self) -> list:
        return self._details

    @description.setter
    def description(self, value):
        self._description = value

    @code.setter
    def code(self, value):
        self._code = value

    def add(self, description, position=None):
        self._details.append({
            "description": description,
            "position": position,
        })

    def is_empty(self):
        return self._details is None or len(self._details) == 0

    def response(self) -> web.Response:
        return web.json_response(
            status=self.code,
            data={
                "error": {
                    "code": self.code,
                    "description": self.description,
                    "details": self.details
                }
            }
        )

    def done(self, code, description) -> web.Response:
        self._code = code
        self._description = description
        return self.response()
