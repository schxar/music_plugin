import asyncio
from typing import Dict, Any, List, Tuple, Optional
from bilibili_api import search
from src.chat.actions.plugin_action import PluginAction, register_action
from src.chat.actions.base_action import ActionActivationType, ChatMode
from src.common.logger_manager import get_logger

logger = get_logger("search_video_action")

@register_action
class BilibiliSearchAction(PluginAction):
    """Bilibili视频搜索动作处理类"""
    
    action_name = "bilibili_search_action"
    action_description = "【定制插件】B站视频搜索功能，支持多种搜索条件和排序方式"
    action_parameters = {
        "keyword": {"type": "str", "description": "搜索关键词"}
    }
    action_require = [
        "当用户需要播放一首指定的歌",
        "用户想听某个歌手的歌曲",
    ]
    enable_plugin = True
    
    focus_activation_type = ActionActivationType.LLM_JUDGE
    normal_activation_type = ActionActivationType.KEYWORD
    
    activation_keywords = ["播放"]
    keyword_case_sensitive = False
    
    llm_judge_prompt = """
判定是否需要使用B站视频搜索动作的条件：
1. 用户输入格式为"播放(歌名)"
2. 用户想要搜索歌曲视频
3. 所有搜索词都会自动添加"异世界情绪"后缀
4. 返回的B站视频链接必须包含完整前缀：https://www.bilibili.com/video/
5. 回复必须含有完整的视频链接
适合使用的情况：
- 任何歌曲搜索请求

绝对不要使用的情况：
1. 纯文字聊天
2. 谈论已存在的视频
3. 用户明确表示不需要搜索时
4. 返回不完整的视频链接
"""
    
    mode_enable = ChatMode.ALL
    parallel_action = False

    def __init__(self, action_data, reasoning, cycle_timers, thinking_id, global_config=None, **kwargs):
        super().__init__(action_data, reasoning, cycle_timers, thinking_id, global_config, **kwargs)

    async def process(self) -> Tuple[bool, str]:
        """处理视频搜索请求"""
        try:
            keyword = f"{self.action_data.get('keyword', '')} 异世界情绪"
            logger.info(f"正在执行B站视频搜索，关键词: {keyword}")
            results = await search.search_by_type(
                keyword=keyword,
                search_type=search.SearchObjectType.VIDEO,
                order_type=search.OrderVideo.TOTALRANK,
                order_sort=0,
                page=1
            )
            logger.info(f"搜索完成，结果数量: {len(results['result']) if results and 'result' in results else 0}")
            
            if not results or 'result' not in results or not results['result']:
                return False, "没有找到搜索结果"
                
            # 格式化结果并提取mid(严格遵循API返回格式)
            formatted_results = []
            for item in results['result']:
                # 从author字段中提取mid
                author_info = item.get('author', {})
                mid = author_info.get('mid', 0) if isinstance(author_info, dict) else 0
                formatted_results.append({
                    "title": item.get("title", ""),
                    "url": item.get("arcurl", ""),
                    "description": item.get("description", ""),
                    "mid": int(mid) if str(mid).isdigit() else 0
                })
            
            # 发送前两个结果
            if formatted_results:
                logger.info(f"准备发送前{min(2, len(formatted_results))}条结果")
                
                # 查找目标mid(488978908)的视频
                target_index = None
                for i in range(min(3, len(formatted_results))):  # 检查前3个结果
                    if formatted_results[i].get("mid") == 488978908:
                        target_index = i
                        break
                
                # 优先发送目标mid的视频，否则发送第一个结果
                send_index = target_index if target_index is not None else 0
                first_url = formatted_results[send_index]["url"]
                if not first_url.startswith("https://www.bilibili.com/video/"):
                    first_url = f"https://www.bilibili.com/video/{first_url.split('/')[-1]}"
                await self.send_message(type="text", data=first_url)
                logger.info("结果发送完成")
                return True, None
            await self.send_message(type="text", data="没有找到搜索结果")
            return False, None
            
        except Exception as e:
            logger.error(f"视频搜索失败: {str(e)}", exc_info=True)
            await self.send_message_by_expressor(f"视频搜索失败: {str(e)}")
            return False, None

    async def search_song(self, song_name: str) -> Optional[Dict[str, str]]:
        """搜索歌曲并返回第一个结果(已弃用，使用主流程处理)"""
        return None