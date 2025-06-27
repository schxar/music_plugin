import asyncio
from typing import Tuple
from src.plugin_system.base.base_action import BaseAction, ActionActivationType, ChatMode
from src.plugin_system.base.component_types import ComponentInfo
from .video_api_action import get_random_video_url
from .generator_tools import generate_rewrite_reply

class BilibiliRandomVideoAction(BaseAction):
    """获取B站随机视频链接的Action"""
    action_name = "bilibili_random_video"
    action_description = "获取B站指定UP主的随机视频链接"
    action_parameters = {}
    action_require = [
        "当用户需要来首歌时调用。"
    ]
    focus_activation_type = ActionActivationType.KEYWORD
    normal_activation_type = ActionActivationType.KEYWORD
    activation_keywords = ["来首歌"]
    keyword_case_sensitive = False
    mode_enable = ChatMode.ALL
    parallel_action = False

    FIXED_UID = 488978908

    async def execute(self) -> Tuple[bool, str]:
        chat_stream = getattr(self, "chat_stream", None)
        url = await get_random_video_url(self.FIXED_UID)
        if url:
            if chat_stream:
                await self.send_text(f"来首歌！B站视频链接：{url}")
                # 调用generate_rewrite_reply进行润色
                status, reply = await generate_rewrite_reply(chat_stream, f"来首歌！B站视频链接：{url}", "B站来首歌视频推荐润色")
                if status and reply:
                    if isinstance(reply, list):
                        for reply_seg in reply:
                            # 只发reply_seg[1]内容
                            if isinstance(reply_seg, (list, tuple)) and len(reply_seg) > 1:
                                await self.send_text(reply_seg[1])
                            elif isinstance(reply_seg, str):
                                await self.send_text(reply_seg)
                    elif isinstance(reply, str):
                        await self.send_text(reply)
            return True, url
        else:
            if chat_stream:
                await self.send_text("未能获取到B站视频链接，请稍后再试。")
            return False, "未获取到视频链接"

    @classmethod
    def get_action_info(cls) -> Tuple[ComponentInfo, type]:
        return super().get_action_info(), cls
