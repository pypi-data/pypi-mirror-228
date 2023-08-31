from functools import wraps

from nonebot_plugin_saa import MessageFactory, Text

from ..errors.error_handler import ErrorHandlers


def handle_error(handlers: ErrorHandlers, silently: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async def receive_error(msg: str):
                if not silently:
                    await MessageFactory(Text(msg)).send(reply=True)

            async with handlers.run_excepting(receive_error):
                return await func(*args, **kwargs)

        return wrapper

    return decorator
