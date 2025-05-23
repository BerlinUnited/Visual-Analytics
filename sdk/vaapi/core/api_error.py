import typing


class ApiError(Exception):
    status_code: typing.Optional[int]
    body: typing.Any

    def __init__(
        self, *, status_code: typing.Optional[int] = None, body: typing.Any = None
    ):
        self.status_code = status_code
        self.body = body

    def __str__(self) -> str:
        return f"status_code: {self.status_code}, body: {self.body}"
