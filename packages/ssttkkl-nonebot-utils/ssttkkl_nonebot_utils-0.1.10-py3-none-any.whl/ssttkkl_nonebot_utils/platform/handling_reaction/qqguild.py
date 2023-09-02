from asyncio import create_task, sleep
from contextlib import asynccontextmanager

from nonebot import logger
from nonebot.adapters.qqguild import Event, Bot, MessageEvent
from nonebot.exception import MatcherException


def add_reaction(bot: Bot, event: MessageEvent, type: int, id: str, delay: float = 0):
    async def _():
        try:
            await sleep(delay)
            await bot.put_message_reaction(channel_id=event.channel_id, message_id=event.id,
                                           type=type, id=id)
        except BaseException as e:
            logger.exception(e)

    create_task(_())


def remove_reaction(bot: Bot, event: MessageEvent, type: int, id: str, delay: float = 0):
    async def _():
        try:
            await sleep(delay)
            await bot.delete_own_message_reaction(channel_id=event.channel_id, message_id=event.id,
                                                  type=type, id=id)
        except BaseException as e:
            logger.exception(e)

    create_task(_())


@asynccontextmanager
async def handling_reaction(bot: Bot, event: Event):
    # 发送reaction时需要等待一下，否则会撞exceed frequency limit
    if not isinstance(event, MessageEvent):
        return

    add_reaction(bot, event, type=2, id="128563")  # 处理中：😳
    try:
        yield
        add_reaction(bot, event, type=2, id="128536", delay=1)  # 处理完毕：😘
    except BaseException as e:
        if not isinstance(e, MatcherException):
            add_reaction(bot, event, type=2, id="128557", delay=1)  # 处理出错：😭
        raise e
    finally:
        remove_reaction(bot, event, type=2, id="128563", delay=2)  # 处理中：😳
