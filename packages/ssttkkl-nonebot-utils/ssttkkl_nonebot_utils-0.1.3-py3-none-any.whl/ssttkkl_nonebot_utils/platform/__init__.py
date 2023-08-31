import importlib

from nonebot import logger

from .func_manager import FuncManagerFactory

platform_func = FuncManagerFactory()

supported_platform = ("onebot.v11", "kaiheila", "qqguild")

for func_name in (
        "is_destination_available",
        "handling_reaction",
        "get_user_nickname",
        "is_group_admin",
        "extract_mention_user",
        "upload_file",
        "send_msgs"
):
    try:
        func_module = importlib.import_module("ssttkkl_nonebot_utils.platform." + func_name)
        for platform in supported_platform:
            try:
                func_module = importlib.import_module(f"ssttkkl_nonebot_utils.platform.{func_name}.{platform}")
                adapter_module = importlib.import_module(f"nonebot.adapters.{platform}")
                platform_func.register(adapter_module.Adapter.get_name(), func_name, getattr(func_module, func_name))
            except ImportError:
                logger.trace(f"failed to register {func_name} for {platform}")

        try:
            func_module = importlib.import_module(f"ssttkkl_nonebot_utils.platform.{func_name}.fallback")
            platform_func.register("fallback", func_name, getattr(func_module, func_name))
        except ImportError:
            logger.trace(f"failed to register {func_name} for fallback")
    except ImportError:
        logger.trace(f"failed to register {func_name} for all platform")

__all__ = ("platform_func",)
