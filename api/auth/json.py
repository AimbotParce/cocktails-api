from datetime import datetime
from functools import wraps
from typing import Callable, Literal, ParamSpec, TypeVar

import flask

from database.models import Device, Group, Nonce, RolePermission, UserGroupRole

from ..serializers.api_response import Err

T = TypeVar("T")
P = ParamSpec("P")

# Receive the device_id, check which group it's in. then check if the user has permission to access the endpoint in that group


def json_requires(*requisites: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Check if the request has the required json fields."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for requisite in requisites:
                if requisite not in flask.request.json:
                    return Err(f"Missing {requisite}").make_response(400)

            return func(*args, **kwargs)

        return wrapper

    return decorator
