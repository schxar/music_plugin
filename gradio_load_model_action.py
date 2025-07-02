

from typing import Tuple
from src.plugin_system.base.base_action import BaseAction, ActionActivationType, ChatMode
from src.plugin_system.base.component_types import ComponentInfo
from .netease_download_tool import download_netease_flac

class GradioLoadModelAction(BaseAction):
    """网易云音乐下载Action"""
    action_name = "netease_download"
    action_description = "下载网易云音乐flac音频到本地cache目录"
    action_parameters = {
        "query": "必填，歌曲名"
    }
    action_require = [
        "当用户需要下载网易云音乐时调用。query为必填。"
    ]
    focus_activation_type = ActionActivationType.ALWAYS
    normal_activation_type = ActionActivationType.ALWAYS
    activation_keywords = ["网易云下载", "下载网易云", "下载歌曲", "下载音乐"]
    keyword_case_sensitive = False
    mode_enable = ChatMode.ALL
    parallel_action = False

    async def execute(self) -> Tuple[bool, str]:
        await self.send_text(f"action_parameters: {self.action_parameters}")
        song_name = self.action_parameters.get("query", "").strip()
        choose = self.action_parameters.get("choose", "1").strip()
        quality = self.action_parameters.get("quality", "9").strip()
        if not song_name or song_name == "必填，歌曲名":
            await self.send_text("未输入歌曲名")
            return False, "未输入歌曲名"
        try:
            flac_file = await download_netease_flac(song_name, choose, quality)
            await self.send_text(f"下载完成: {flac_file}")
            return True, f"下载完成: {flac_file}"
        except Exception as e:
            await self.send_text(f"下载失败: {e}")
            return False, f"下载失败: {e}"

    @classmethod
    def get_action_info(cls) -> Tuple[ComponentInfo, type]:
        return super().get_action_info(), cls
