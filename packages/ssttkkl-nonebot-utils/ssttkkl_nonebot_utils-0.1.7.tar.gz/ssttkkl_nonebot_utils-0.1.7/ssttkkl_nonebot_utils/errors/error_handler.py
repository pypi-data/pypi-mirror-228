from contextlib import asynccontextmanager
from inspect import isawaitable
from typing import Type, Tuple, Union, Optional, Callable, List, Awaitable, Any

from nonebot import logger
from nonebot.exception import MatcherException, ActionFailed
from nonebot.internal.matcher import current_matcher

from ssttkkl_nonebot_utils.errors.errors import BadRequestError, QueryError

T_EXCEPTABLE = Union[Type[BaseException], Tuple[Type[BaseException]]]
T_ERROR_HANDLER = Union[Callable[[BaseException], str], Callable[[BaseException], Awaitable[str]]]
T_AFTER_ERROR_HANDLER = Callable[[BaseException, str], Any]

_after_error_handler = []


def invoke_after_error(func: T_AFTER_ERROR_HANDLER):
    _after_error_handler.append(func)
    return func


class ErrorHandlers:
    def __init__(self):
        self.handlers: List[Tuple[T_EXCEPTABLE, T_ERROR_HANDLER]] = []

    def register(
            self, error_type: T_EXCEPTABLE,
            func: Optional[T_ERROR_HANDLER] = None
    ):
        def decorator(func: Optional[T_ERROR_HANDLER]):
            self.handlers.append((error_type, func))
            return func

        if func is not None:
            decorator(func)
        else:
            return decorator

    @asynccontextmanager
    async def run_excepting(self, receive_error_message: Optional[
        Union[Callable[[str], Any],
              Callable[[str], Awaitable[Any]]]
    ] = None):
        matcher = None
        try:
            matcher = current_matcher.get()
        except LookupError:
            pass

        try:
            yield
        except MatcherException as e:
            raise e
        except ActionFailed as e:
            # 避免当发送消息错误时再尝试发送
            logger.exception(e)
        except (BadRequestError, QueryError) as e:
            msg = e.message

            help_info = getattr(matcher, "__help_info__", None)
            if help_info is not None:
                msg += f"\n\n指令用法：{help_info}"

            coro = receive_error_message(msg)
            if isawaitable(coro):
                await coro
        except BaseException as e:
            try:
                for excs, handler in self.handlers:
                    if not isinstance(excs, tuple):
                        excs = (excs,)

                    for exc in excs:
                        if isinstance(e, exc):
                            msg = handler(e)
                            if isawaitable(msg):
                                msg = await msg

                            if msg is not None:
                                coro = receive_error_message(msg)
                                if isawaitable(coro):
                                    await coro
                            return

                # fallback
                logger.exception(e)
                coro = receive_error_message(f"内部错误：{type(e)}{str(e)}")
                if isawaitable(coro):
                    await coro
            finally:
                for h in _after_error_handler:
                    coro = h()
                    if isawaitable(coro):
                        await coro
