import random
from typing import Tuple
from src.chat.actions.plugin_action import PluginAction, register_action

@register_action
class RandomSongAction(PluginAction):
    """随机点歌Action"""
    
    async def process(self) -> Tuple[bool, str]:
        """随机选择一首歌"""
        video_list = await self._load_cached_videos()
        if not video_list:
            return False, "没有可用的视频列表"
            
        selected = random.choice(video_list)
        return True, self._format_video_info(selected)
