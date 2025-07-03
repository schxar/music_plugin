

from typing import Tuple
from src.plugin_system.base.base_action import BaseAction, ActionActivationType, ChatMode
from src.plugin_system.base.component_types import ComponentInfo
from .netease_download_tool import download_netease_flac

class SingAction(BaseAction):
    """调用SOVITS处理网易云音乐下载的FLAC实现AI翻唱"""
    action_name = "sing"
    action_description = "调用SOVITS处理网易云音乐下载的FLAC实现AI翻唱"
    action_parameters = {
        "song_name": "必填，歌曲名"
    }
    action_require = [
        "当用户需要你唱歌时调用。song_name为必填。"
    ]
    focus_activation_type = ActionActivationType.ALWAYS
    normal_activation_type = ActionActivationType.ALWAYS
    activation_keywords = ["唱歌", "AI翻唱", "帮我唱", "唱一首", "AI唱歌"]
    keyword_case_sensitive = False
    mode_enable = ChatMode.ALL
    parallel_action = True

    async def execute(self) -> Tuple[bool, str]:
        import aiohttp
        await self.send_text(f"action_parameters: {self.action_parameters}")
        song_name = self.action_parameters.get("song_name", "").strip()
        if not song_name or song_name == "必填，歌曲名":
            await self.send_text("未输入歌曲名")
            return False, "未输入歌曲名"
        choose = "1"
        quality = "1"
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "song": song_name,
                    "choose": choose,
                    "quality": quality
                }
                async with session.post("http://127.0.0.1:5211", data=payload) as resp:
                    text = await resp.text()
            # 尝试提取最后生成音频的路径
            import re
            match = re.search(r"最终合成完成: (.+)", text)
            if match:
                final_path = match.group(1).strip()
                await self.send_text(f"最终音频路径: {final_path}")
                return True, final_path
            else:
                await self.send_text(f"处理输出: {text}")
                return False, f"未找到最终音频路径，输出如下：\n{text}"
        except Exception as e:
            await self.send_text(f"处理失败: {e}")
            return False, f"处理失败: {e}"

    @classmethod
    def get_action_info(cls) -> Tuple[ComponentInfo, type]:
        return super().get_action_info(), cls
