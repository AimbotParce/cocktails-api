import inspect
from functools import wraps
from typing import Callable, Literal, ParamSpec, TypeVar

import flask

from database.exceptions import *
from database.managers import DevicesManager, GroupsManager, PermissionsManager

from ..serializers.api_response import Err

T = TypeVar("T")
P = ParamSpec("P")

# Receive the device_id, check which group it's in. then check if the user has permission to access the endpoint in that group


LEVELS = {None: 0, "group": 1, "device": 2}


def check_auth(level: Literal[None, "group", "device"] = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Check if the nonce is valid and if the user has permission to access the endpoint in the group or device.
    If check_group is True, it will also check if the user has permission to access the endpoint in the group.
    """
    if not level in [None, "group", "device"]:
        raise ValueError(f"Invalid level: {level}")

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        endpoint = func.__name__

        if LEVELS[level] >= LEVELS["group"]:
            argspec = inspect.getfullargspec(func)
            owner_arg_pos = argspec.args.index("owner")
            group_arg_pos = argspec.args.index("group")
            if LEVELS[level] >= LEVELS["device"]:
                device_arg_pos = argspec.args.index("device_id")

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            nonce = flask.request.headers.get("Authorization")
            with PermissionsManager() as permissions:
                if not permissions.validate_nonce_endpoint(nonce, endpoint):
                    return Err("Unauthorized").make_response(401)
                user_id = permissions.get_nonce_user_id(nonce)

            if LEVELS[level] >= LEVELS["group"]:
                with GroupsManager() as groups:
                    owner = args[owner_arg_pos]
                    group_name = args[group_arg_pos]
                    try:
                        group_id = groups.get_group_from_owner_and_name(owner, group_name)
                    except UserNotExists:
                        return Err("Group owner not found").make_response(404)
                    except GroupNotExists:
                        return Err("Group not found").make_response(404)

                with PermissionsManager() as permissions:
                    # Check if the user has permission to access the endpoint in that group
                    try:
                        if not permissions.validate_user_group_endpoint(user_id, group_id, endpoint):
                            return Err("Unauthorized").make_response(401)
                    except UserNotInGroup:
                        return Err("Unauthorized").make_response(401)

                if LEVELS[level] >= LEVELS["device"]:
                    device_id = args[device_arg_pos]
                    with DevicesManager() as devices:
                        try:
                            device_group_id = devices.get_device_group_id(device_id)
                        except DeviceNotExists:
                            return Err("Device not found").make_response(404)

                        if not device_group_id == group_id:
                            return Err("Device not in group").make_response(400)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_user_id_from_nonce() -> int | None:
    "Read the authorization header and return the user if the nonce is valid"
    nonce = flask.request.headers.get("Authorization")
    with PermissionsManager() as permissions:
        try:
            user_id = permissions.get_nonce_user_id(nonce)
        except InvalidNonce:
            return None
    return user_id
