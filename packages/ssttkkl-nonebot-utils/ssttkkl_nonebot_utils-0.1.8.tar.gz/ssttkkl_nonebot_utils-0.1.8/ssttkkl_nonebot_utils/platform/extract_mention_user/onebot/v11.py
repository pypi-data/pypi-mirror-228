from typing import Optional

from nonebot.adapters.onebot.v11 import MessageSegment


async def extract_mention_user(seg: MessageSegment) -> Optional[str]:
    if seg.type == 'at':
        return seg.data['qq']
    else:
        return None
