from typing import Any, Callable, ParamSpec, TypeVar

import flask

R = TypeVar("R", bound="Response")
P = ParamSpec("P")


class undefined:
    pass


class Response:
    ok: bool
    message: str
    data: Any
    status: int = 200

    def __init__(self, data: Any = None, message: str = "", **dict_data: Any):
        if data and dict_data:
            raise ValueError("You cannot pass both list and dictionary data")
        if data is not None:
            self.data = data
        elif dict_data:
            self.data = dict_data
        self.message = message

    @property
    def json(self):
        if hasattr(self, "data"):
            return {"ok": self.ok, "message": self.message, "data": self.data}
        else:
            return {"ok": self.ok, "message": self.message}

    def status(self, status: int):
        self.status = status
        return self


class Ok(Response):
    ok = True


class Err(Response):
    ok = False

    def __init__(self, message: str = "", data: Any = None, **dict_data: Any):
        super().__init__(message=message, data=data, **dict_data)


def make_response(foo: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        response = foo(*args, **kwargs)
        return flask.make_response(response.json, response.status)

    return wrapper
