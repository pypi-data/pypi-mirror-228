from nonebot import get_driver

default_command_start: str = next(iter(get_driver().config.command_start))

__all__ = ("default_command_start",)
