import asyncio
import re
from typing import Tuple, Optional
from bilibili_api import video, Credential
from src.chat.actions.plugin_action import PluginAction, register_action
from src.chat.actions.base_action import ActionActivationType, ChatMode
from src.common.logger_manager import get_logger

logger = get_logger("bvid_parse_action")

@register_action
class BvidParseAction(PluginAction):
    """B站视频解析动作，支持AV/BV号和URL"""

    action_name = "bvid_parse_action"
    action_description = "解析B站视频(AV/BV号或URL)并返回详细信息"
    action_parameters = {
        "input": "B站视频AV/BV号或URL"
    }
    action_require = [
        "当输入包含av/BV号时使用",
        "当输入是B站视频链接时使用"
    ]
    enable_plugin = True
    _credential_config_path = "config/bilibili_credential.json"
    
    focus_activation_type = ActionActivationType.LLM_JUDGE
    normal_activation_type = ActionActivationType.KEYWORD
    
    activation_keywords = ["BV", "AV", "bilibili.com"]
    keyword_case_sensitive = False
    
    llm_judge_prompt = """
判定是否需要使用B站视频解析动作的条件：
1. 输入包含AV号(如av123456)
2. 输入包含BV号(如BV1xx4y1y7xx)
3. 输入包含bilibili.com视频链接

适合使用的情况：
- "解析下这个视频：BV1xx4y1y7xx"
- "看看这个链接内容：https://www.bilibili.com/video/BV1xx4y1y7xx"
- "这个av123456视频讲了什么"

绝对不要使用的情况：
1. 纯文字聊天无视频标识
2. 非B站视频链接
"""
    
    mode_enable = ChatMode.ALL
    parallel_action = False

    def __init__(self, action_data, reasoning, cycle_timers, thinking_id, global_config=None, **kwargs):
        super().__init__(action_data, reasoning, cycle_timers, thinking_id, global_config, **kwargs)
        logger.info(f"{self.log_prefix} 初始化B站视频解析动作")

    async def process(self) -> Tuple[bool, str]:
        """处理视频解析请求"""
        input_text = self.action_data.get("input", "")
        logger.info(f"{self.log_prefix} 解析输入: {input_text}")
        
        # 提取视频ID
        video_id = self._extract_video_id(input_text)
        if not video_id:
            await self.send_message_by_expressor("未检测到有效的B站视频AV/BV号或链接")
            return False, "无效的视频标识"
            
        await self.send_message_by_expressor(f"正在解析视频 {video_id}...")
        
        try:
            # 获取凭证
            credential = await self._get_credential()
            if credential:
                logger.info(f"{self.log_prefix} 使用登录凭证")
            
            # 创建视频对象
            v = video.Video(bvid=video_id if video_id.startswith("BV") else None,
                          aid=int(video_id[2:]) if video_id.startswith("av") else None,
                          credential=credential)
            
            # 获取视频信息
            info = await v.get_info()
            logger.info(f"{self.log_prefix} 获取到视频信息: {info.get('title')}")
            
            # 构建返回消息
            message = self._build_video_message(info)
            await self.send_message(type="text", data=message)
            
            # 发送封面图
            if info.get('pic'):
                await self.send_message(type="image", data=info['pic'])
                
            return True, "视频解析成功"
            
        except Exception as e:
            logger.error(f"{self.log_prefix} 解析视频失败: {str(e)}", exc_info=True)
            await self.send_message_by_expressor(f"解析视频失败: {str(e)}")
            return False, f"视频解析失败: {str(e)}"

    def _extract_video_id(self, text: str) -> Optional[str]:
        """从文本提取AV/BV号或视频URL中的标识"""
        # 匹配BV号
        bv_match = re.search(r"(BV[a-zA-Z0-9]{10})", text)
        if bv_match:
            return bv_match.group(1)
            
        # 匹配AV号
        av_match = re.search(r"(av\d+)", text, re.IGNORECASE)
        if av_match:
            return av_match.group(1).lower()
            
        # 匹配视频URL
        url_match = re.search(
            r"bilibili\.com/video/(BV[a-zA-Z0-9]{10}|av\d+)",
            text,
            re.IGNORECASE
        )
        if url_match:
            return url_match.group(1).lower()
            
        return None

    def _build_video_message(self, info: dict) -> str:
        """构建视频信息消息"""
        title = info.get('title', '未知标题')
        desc = info.get('desc', '无描述')[:100] + "..." if info.get('desc') else '无描述'
        duration = info.get('duration', 0)
        minutes, seconds = divmod(duration, 60)
        owner = info.get('owner', {}).get('name', '未知UP主')
        stat = info.get('stat', {})
        
        return (
            f"📺 视频标题: {title}\n"
            f"👤 UP主: {owner}\n"
            f"⏱️ 时长: {minutes}分{seconds}秒\n"
            f"📊 播放: {stat.get('view', 0)} | "
            f"弹幕: {stat.get('danmaku', 0)} | "
            f"点赞: {stat.get('like', 0)}\n"
            f"📝 简介: {desc}\n"
            f"🔗 链接: https://www.bilibili.com/video/{info.get('bvid') or 'av'+str(info.get('aid'))}"
        )

    async def _get_credential(self) -> Optional[Credential]:
        """获取B站凭证(复用VideoApiAction逻辑)"""
        try:
            if os.path.exists(self._credential_config_path):
                with open(self._credential_config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return Credential(**config)
            return None
        except Exception as e:
            logger.warning(f"{self.log_prefix} 读取凭证配置失败: {str(e)}")
            return None
