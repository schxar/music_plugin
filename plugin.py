import http.client
import json
from .generator_tools import generate_rewrite_reply

class NapcatClient:
    def send_group_text(self, group_id: int, text: str):
        """
        发送文本消息到指定群聊。
        :param group_id: 群号
        :param text: 文本内容
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": text
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_group_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        try:
            resp_json = json.loads(data.decode("utf-8"))
            success = resp_json.get("status") == "ok" and resp_json.get("retcode") == 0
            return success, resp_json
        except Exception:
            return False, None

    def send_private_text(self, user_id: int, text: str):
        """
        发送文本消息到指定私聊。
        :param user_id: 用户ID
        :param text: 文本内容
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": text
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_private_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        try:
            resp_json = json.loads(data.decode("utf-8"))
            success = resp_json.get("status") == "ok" and resp_json.get("retcode") == 0
            return success, resp_json
        except Exception:
            return False, None

    def __init__(self, host="127.0.0.1", port=4998):
        self.host = host
        self.port = port

    def send_group_music_card(self, group_id: int, music_type: str, music_id: str):
        """
        发送音乐小程序卡片到指定群聊。
        :param group_id: 群号
        :param music_type: 音乐平台类型（如 '163'）
        :param music_id: 音乐ID
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "music",
                    "data": {
                        "type": music_type,
                        "id": music_id
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_group_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        try:
            resp_json = json.loads(data.decode("utf-8"))
            success = resp_json.get("status") == "ok" and resp_json.get("retcode") == 0
            return success, resp_json
        except Exception:
            return False, None

    def send_group_record(self, group_id: int, file_path: str):
        """
        发送语音消息到指定群聊。
        :param group_id: 群号
        :param file_path: 语音文件路径（本地或网络）
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "group_id": group_id,
            "message": [
                {
                    "type": "record",
                    "data": {
                        "file": file_path
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_group_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        try:
            resp_json = json.loads(data.decode("utf-8"))
            success = resp_json.get("status") == "ok" and resp_json.get("retcode") == 0
            return success, resp_json
        except Exception:
            return False, None

    def send_private_music_card(self, user_id: int, music_type: str, music_id: str):
        """
        发送音乐小程序卡片到指定私聊。
        :param user_id: 用户ID
        :param music_type: 音乐平台类型（如 '163'）
        :param music_id: 音乐ID
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "music",
                    "data": {
                        "type": music_type,
                        "id": music_id
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_private_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        try:
            resp_json = json.loads(data.decode("utf-8"))
            success = resp_json.get("status") == "ok" and resp_json.get("retcode") == 0
            return success, resp_json
        except Exception:
            return False, None

    def send_private_record(self, user_id: int, file_path: str):
        """
        发送语音消息到指定私聊。
        :param user_id: 用户ID
        :param file_path: 语音文件路径（本地或网络）
        :return: Napcat响应内容
        """
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps({
            "user_id": user_id,
            "message": [
                {
                    "type": "record",
                    "data": {
                        "file": file_path
                    }
                }
            ]
        })
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/send_private_msg", payload, headers)
        res = conn.getresponse()
        data = res.read()
        try:
            resp_json = json.loads(data.decode("utf-8"))
            success = resp_json.get("status") == "ok" and resp_json.get("retcode") == 0
            return success, resp_json
        except Exception:
            return False, None


from typing import Any, Tuple, List, Type

async def generate_rewrite_reply(chat_stream: Any, raw_reply: str, reason: str) -> Tuple[bool, Any]:
    """
    调用 generator_api.rewrite_reply 生成回复，供插件统一调用。
    :param chat_stream: 聊天流对象
    :param raw_reply: 原始回复文本
    :param reason: 生成回复的理由
    :return: (状态, 消息)
    """
    return await generator_api.rewrite_reply(
        chat_stream=chat_stream,
        reply_data={
            "raw_reply": raw_reply,
            "reason": reason,
        }
    )
import aiohttp
import json
import random
import re

from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.apis.plugin_register_api import register_plugin
from src.plugin_system.base.base_action import BaseAction, ActionActivationType, ChatMode
from src.plugin_system.base.base_command import BaseCommand
from src.plugin_system.base.component_types import ComponentInfo
from src.plugin_system.base.config_types import ConfigField
from src.plugin_system.apis import generator_api
from src.plugin_system.apis import database_api
from src.plugin_system.apis import config_api
from src.common.database.database_model import Messages, PersonInfo
from src.person_info.person_info import get_person_id_by_person_name
from src.common.logger import get_logger
from PIL import Image
from typing import Tuple, Dict, Optional, List, Any, Type
from pathlib import Path
import traceback
import tomlkit
import json
import random
import asyncio
import aiohttp
import base64
import toml
import io
import os
import re
from src.plugin_system.apis import send_api, chat_api
from src.plugin_system import (
    BasePlugin, register_plugin, BaseAction, BaseCommand,
    ComponentInfo, ActionActivationType, ChatMode
)
from src.plugin_system.base.config_types import ConfigField
from src.common.logger import get_logger
from src.chat.message_receive.chat_stream import ChatStream
# from .bilibili_random_video_action import BilibiliRandomVideoAction  # 延迟导入，避免加载时报错
#from .gradio_load_model_action import SingAction  # 导入SOVITS翻唱Action

logger = get_logger("music")

# ===== 智能消息发送工具 =====
# 计数器: (chat_id, song_name) -> choose
choose_counter = {}

async def smart_send(chat_stream, message_data):
    """智能发送不同类型的消息，并返回实际发包内容"""
    message_type = message_data.get("type", "text")
    content = message_data.get("content", "")
    options = message_data.get("options", {})
    target_id = (chat_stream.group_info.group_id if getattr(chat_stream, 'group_info', None)
                else chat_stream.user_info.user_id)
    is_group = getattr(chat_stream, 'group_info', None) is not None
    # 调试用，记录实际发包内容
    packet = {
        "message_type": message_type,
        "content": content,
        "target_id": target_id,
        "is_group": is_group,
        "typing": options.get("typing", False),
        "reply_to": options.get("reply_to", ""),
        "display_message": options.get("display_message", "")
    }
    print(f"[调试] smart_send 发包内容: {json.dumps(packet, ensure_ascii=False)}")
    # 实际发送
    success = await send_api.custom_message(
        message_type=message_type,
        content=content,
        target_id=target_id,
        is_group=is_group,
        typing=options.get("typing", False),
        reply_to=options.get("reply_to", ""),
        display_message=options.get("display_message", "")
    )
    return success, packet

# ===== Action组件 =====

class MusicSearchAction(BaseAction):
    """音乐搜索Action - 智能音乐推荐"""

    action_name = "music_search"
    action_description = "搜索并推荐音乐"

    # 关键词激活
    focus_activation_type = ActionActivationType.KEYWORD
    normal_activation_type = ActionActivationType.KEYWORD
    
    activation_keywords = ["音乐", "歌曲", "点歌", "听歌", "music", "song"]
    keyword_case_sensitive = False

    action_parameters = {
        "song_name": "要搜索的歌曲名称",
        "quality": "音质要求(1-9，可选)",
        "direct_url": "是否直接发送直链（布尔，true为直链，false为先尝试卡片,默认为false）",
        "choose": "选择发送该搜索词结果的第几个（整数，1为第一个，2为第二个，依此类推，默认为1）"
    }
    action_require = [
        "仅当用户明确表达想要听音乐、点歌、或询问音乐相关信息时才调用本动作。",
        "如果用户只是随口提到音乐、歌曲等词汇，但没有明确要求点歌，不要执行本动作。",
        "请勿在没有新用户输入的情况下重复执行本动作，除非用户有新的点歌请求。",
        "如果用户已经点过歌，除非用户明确要求再次点歌，否则不要连续执行本动作。",
        "如果用户没有指定歌曲名，请主动询问用户想听什么歌，不要随意推荐。",
        "如用户明确要求直链，则发送直链，否则优先尝试发送音乐卡片。"
    ]
    associated_types = ["text"]

    async def _fetch_music_info_with_retry(self, song_name, quality, api_url):
        import asyncio
        choose_input = self.action_data.get("choose", None)
        try:
            choose_input = int(choose_input)
            if choose_input < 1:
                choose_input = 1
        except Exception:
            choose_input = None
        if choose_input:
            tries = [choose_input, 1, 2, 3]
            # 去重且保持顺序
            seen = set()
            tries = [x for x in tries if not (x in seen or seen.add(x))]
        else:
            tries = [1, 2, 3]
        for idx, c in enumerate(tries):
            await asyncio.sleep(3) if idx > 0 else None
            async with aiohttp.ClientSession() as session:
                params = {
                    "word": song_name,
                    "quality": quality,
                    "choose": c
                }
                async with session.get(f"{api_url}/v2/music/netease", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == 200:
                            return True, data.get("data", {}), c
        # 只要不是成功就继续下一次
        return False, None, tries[-1]

    def _get_target_info(self, chat_stream):
        """获取目标ID和群聊标志"""
        if chat_stream:
            target_id = str(chat_stream.group_info.group_id) if getattr(chat_stream, "group_info", None) else str(chat_stream.user_info.user_id)
            is_group = getattr(chat_stream, "group_info", None) is not None
            return target_id, is_group
        return None, False

    async def _send_ask_song_name(self, chat_stream):
        if chat_stream:
            await self.send_text("请告诉我你想听什么歌曲~")

    async def _handle_api_success(self, music_info, direct_url=False):
        await self._send_music_info(music_info, direct_url)
        return True, f"找到音乐: {music_info.get('song', '未知')}"

    async def _handle_api_failure(self, chat_stream):
        if chat_stream:
            await self.send_text("搜索失败: 未找到合适的音乐，请稍后再试")
        return False, "API返回错误"

    async def _handle_exception(self, chat_stream, e):
        logger.error(f"音乐搜索失败: {e}")
        if chat_stream:
            await self.send_text("搜索音乐时出现错误，请稍后再试")
        return False, f"搜索失败: {str(e)}"

    async def execute(self) -> Tuple[bool, str]:
        """执行音乐搜索"""
        song_name = self.action_data.get("song_name", "")
        quality = self.action_data.get("quality", "9")  # 默认最高音质
        direct_url = self.action_data.get("direct_url", False)
        chat_stream = getattr(self, "chat_stream", None)
        if not song_name:
            await self._send_ask_song_name(chat_stream)
            return True, "请求用户输入歌曲名"
        api_url = self.get_config("api.base_url", "https://api.vkeys.cn")
        try:
            success, music_info, choose_used = await self._fetch_music_info_with_retry(song_name, quality, api_url)
            if success and music_info:
                return await self._handle_api_success(music_info, direct_url)
            else:
                return await self._handle_api_failure(chat_stream)
        except Exception as e:
            return await self._handle_exception(chat_stream, e)

    async def _send_music_info(self, music_info: dict, direct_url=False):
        song = music_info.get("song", "未知歌曲")
        url = music_info.get("url", "")
        chat_stream = getattr(self, "chat_stream", None)
        if direct_url:
            if chat_stream and url:
                await self.send_text(f"播放链接：{song} {url}")
            return
        napcat_card_sent = False
        # Napcat音乐卡片优先尝试
        try:
            group_info = getattr(chat_stream, "group_info", None) if chat_stream else None
            group_id = getattr(group_info, "group_id", None)
            user_id = getattr(chat_stream.user_info, "user_id", None) if chat_stream else None
            music_id = (
                music_info.get("id") or
                music_info.get("songid") or
                music_info.get("songId")
            )
            # from .napcat_client import NapcatClient
            client = NapcatClient()
            resp = None
            if group_id is not None and music_id:
                try:
                    group_id_int = int(group_id)
                except Exception:
                    group_id_int = group_id
                resp = client.send_group_music_card(group_id=group_id_int, music_type="163", music_id=str(music_id))
            elif user_id is not None and music_id:
                try:
                    user_id_int = int(user_id)
                except Exception:
                    user_id_int = user_id
                resp = client.send_private_music_card(user_id=user_id_int, music_type="163", music_id=str(music_id))
            if resp:
                logger.info(f"Napcat音乐卡片发送响应: {resp}")
                try:
                    success, resp_json = resp
                    if success and resp_json and resp_json.get("status") == "ok" and resp_json.get("retcode") == 0:
                        napcat_card_sent = True
                        # 发送成功后调用generator生成消息
                        # from .generator_tools import generate_rewrite_reply
                        if chat_stream:
                            result_status, result_message = await generator_api.rewrite_reply(
                                chat_stream=chat_stream,
                                reply_data={
                                    "raw_reply": f"Napcat音乐卡片发送成功：{song}",
                                    "reason": "music_plugin Napcat卡片发送成功提示润色"
                                }
                            )
                            if result_status:
                                for reply_seg in result_message:
                                    data = reply_seg[1]
                                    await self.send_text(data)
                                    await asyncio.sleep(1.0)
                            else:
                                await self.send_text(f"Napcat音乐卡片发送成功：{song}")
                except Exception as e:
                    logger.warning(f"Napcat响应解析失败: {e}")
        except Exception as e:
            logger.warning(f"Napcat音乐卡片发送失败: {e}")
        # 只有Napcat卡片未成功时才发直达链接
        if not napcat_card_sent and chat_stream and url:
            await self.send_text(f"播放链接：{song} {url}")

# ===== Command组件 =====

class MusicCommand(BaseCommand):
    """音乐点歌Command - 直接点歌命令"""

    command_name = "music"
    command_description = "点歌命令"
    command_pattern = r"^/music\s+(?P<song_name>.+)$"  # 用命名组
    command_help = "点歌命令，用法：/music 歌曲名"
    command_examples = ["/music 勾指起誓", "/music 晴天"]
    intercept_message = True

    async def _fetch_music_info_with_retry(self, song_name, quality, api_url):
        import asyncio
        tries = [1, 2, 3]  # 依次尝试1、2、3
        for idx, c in enumerate(tries):
            await asyncio.sleep(3) if idx > 0 else None
            async with aiohttp.ClientSession() as session:
                params = {
                    "word": song_name,
                    "quality": quality,
                    "choose": c
                }
                async with session.get(f"{api_url}/v2/music/netease", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == 200:
                            return True, data.get("data", {}), c
        # 只要不是成功就继续下一次
        return False, None, tries[-1]

    async def execute(self) -> Tuple[bool, str]:
        # 只在标准 Action 场景下用，直接依赖 self.chat_stream
        song_name = (self.matched_groups or {}).get("song_name", "")
        chat_stream = getattr(self, "chat_stream", None)
        if not song_name:
            if chat_stream:
                target_id = str(chat_stream.group_info.group_id) if getattr(chat_stream, "group_info", None) else str(chat_stream.user_info.user_id)
                is_group = getattr(chat_stream, "group_info", None) is not None
                await send_api.custom_message(
                    message_type="text",
                    content="请输入正确的格式：/music 歌曲名",
                    target_id=target_id,
                    is_group=is_group
                )
            return False, "格式错误"
        quality = self.get_config("music.default_quality", "9")
        api_url = self.get_config("api.base_url", "https://api.vkeys.cn")
        try:
            success, music_info, choose_used = await self._fetch_music_info_with_retry(song_name, quality, api_url)
            if success and music_info:
                await self._send_detailed_music_info(music_info)
                return True, f"点歌成功: {music_info.get('song', '未知')} (choose={choose_used})"
            else:
                if chat_stream:
                    target_id = str(chat_stream.group_info.group_id) if getattr(chat_stream, "group_info", None) else str(chat_stream.user_info.user_id)
                    is_group = getattr(chat_stream, "group_info", None) is not None
                    await send_api.custom_message(
                        message_type="text",
                        content="❌ 搜索失败: 未找到合适的音乐，请稍后再试",
                        target_id=target_id,
                        is_group=is_group
                    )
                return False, "搜索失败"
        except Exception as e:
            logger.error(f"点歌失败: {e}")
            if chat_stream:
                target_id = str(chat_stream.group_info.group_id) if getattr(chat_stream, "group_info", None) else str(chat_stream.user_info.user_id)
                is_group = getattr(chat_stream, "group_info", None) is not None
                await send_api.custom_message(
                    message_type="text",
                    content=f"❌ 点歌失败，请稍后再试\n错误信息: {e}",
                    target_id=target_id,
                    is_group=is_group
                )
            return False, f"点歌失败: {str(e)}"

    async def _send_detailed_music_info(self, music_info: dict):
        # from .generator_tools import generate_rewrite_reply
        if not isinstance(music_info, dict):
            return
        song = music_info.get("song", "未知歌曲")
        singer = music_info.get("singer", "未知歌手") 
        album = music_info.get("album", "未知专辑")
        quality = music_info.get("quality", "未知音质")
        interval = music_info.get("interval", "未知时长")
        size = music_info.get("size", "未知大小")
        kbps = music_info.get("kbps", "未知码率")
        cover = music_info.get("cover", "")
        link = music_info.get("link", "")
        url = music_info.get("url", "")
        message = f"🎵 【点歌成功】\n\n"
        message += f"🎤 歌曲：{song}\n"
        message += f"🎙️ 歌手：{singer}\n"
        message += f"💿 专辑：{album}\n"
        message += f"⏱️ 时长：{interval}\n"
        message += f"🎯 音质：{quality}\n"
        message += f"📦 大小：{size}\n"
        message += f"📊 码率：{kbps}\n"
        if link:
            message += f"🔗 网易云链接：{link}\n"
        if url:
            message += f"播放链接：{url}\n"
        chat_stream = getattr(self, "chat_stream", None)
        if chat_stream is None and hasattr(self, "message") and hasattr(self.message, "chat_stream"):
            chat_stream = self.message.chat_stream
        if chat_stream is not None:
            status, reply = await generate_rewrite_reply(chat_stream, message, "music_plugin详细音乐信息美化")
        else:
            status, reply = False, None
        if chat_stream:
            if status and reply:
                await self.send_text(reply)
            else:
                group_info = getattr(chat_stream, "group_info", None)
                if group_info and getattr(group_info, "group_id", None):
                    target_id = group_info.group_id
                else:
                    target_id = getattr(chat_stream.user_info, "user_id", None)
                is_group = group_info is not None
                if target_id is not None:
                    await send_api.custom_message(
                        message_type="text",
                        content=message,
                        target_id=target_id,
                        is_group=is_group
                    )
        # 如果有封面图片，可以发送图片
        # 已移除封面图片发送逻辑（小程序卡片自带封面）
        # ===== 新增：发送音乐小程序卡片到群聊（Napcat 4998） =====
        napcat_card_sent = False
        try:
        # from .napcat_client import NapcatClient
            group_info = getattr(chat_stream, "group_info", None) if chat_stream else None
            group_id = getattr(group_info, "group_id", None)
            user_id = getattr(chat_stream.user_info, "user_id", None) if chat_stream else None
            music_id = music_info.get("id") or music_info.get("songid") or music_info.get("songId")
            client = NapcatClient()
            resp = None
            if group_id is not None and music_id:
                try:
                    group_id_int = int(group_id)
                except Exception:
                    group_id_int = group_id
                resp = client.send_group_music_card(group_id=group_id_int, music_type="163", music_id=str(music_id))
            elif user_id is not None and music_id:
                try:
                    user_id_int = int(user_id)
                except Exception:
                    user_id_int = user_id
                resp = client.send_private_music_card(user_id=user_id_int, music_type="163", music_id=str(music_id))
            if resp:
                logger.info(f"Napcat音乐卡片发送响应: {resp}")
                try:
                    resp_json = json.loads(resp)
                    if resp_json.get("status") == "ok" and resp_json.get("retcode") == 0:
                        napcat_card_sent = True
                        # 发送成功后调用generator生成消息
                        if chat_stream:
                            result_status, result_message = await generator_api.rewrite_reply(
                                chat_stream=chat_stream,
                                reply_data={
                                    "raw_reply": f"Napcat音乐卡片发送成功：{song}",
                                    "reason": "music_plugin Napcat卡片发送成功提示"
                                }
                            )
                            if result_status:
                                for reply_seg in result_message:
                                    data = reply_seg[1]
                                    await self.send_text(data)
                                    await asyncio.sleep(1.0)
                            else:
                                await self.send_text(f"Napcat音乐卡片发送成功：{song}")
                except Exception as e:
                    logger.warning(f"Napcat响应解析失败: {e}")
        except Exception as e:
            logger.warning(f"Napcat音乐卡片发送失败: {e}")
        # ===== 只在卡片未成功时发送url，不再发送封面 =====
        if not napcat_card_sent:
            url = music_info.get("url", "")
            if url and chat_stream:
                group_info = getattr(chat_stream, "group_info", None)
                if group_info and getattr(group_info, "group_id", None):
                    target_id = group_info.group_id
                else:
                    target_id = getattr(chat_stream.user_info, "user_id", None)
                is_group = group_info is not None
                if target_id is not None:
                    await send_api.custom_message(
                        message_type="text",
                        content=f"播放链接：{song} {url}",
                        target_id=target_id,
                        is_group=is_group
                    )

# ===== 插件注册 =====

from .napcat_client import NapcatClient

class SingAction(BaseAction):
    """调用SOVITS处理网易云音乐下载的FLAC实现AI翻唱或TTS文本转语音"""
    action_name = "sing"
    action_description = "调用SOVITS处理网易云音乐下载的FLAC实现AI翻唱或TTS文本转语音"
    action_parameters = {
        "song_name": "必填，歌曲名或TTS文本",
        "tts_mode": "可选，布尔值，为True时song_name作为TTS文本"
    }
    action_require = [
        "当用户需要你唱歌时调用。song_name为必填。当有人让你说话时tts_mode为True,走TTS文本转语音。"
        "在你自己发言说 发了 之后,不需要再调用一次tts语音"
    ]
    focus_activation_type = ActionActivationType.ALWAYS
    normal_activation_type = ActionActivationType.ALWAYS
    activation_keywords = ["唱歌", "AI翻唱", "帮我唱", "唱一首", "AI唱歌"]
    keyword_case_sensitive = False
    mode_enable = ChatMode.ALL
    parallel_action = True

    async def execute(self) -> Tuple[bool, str]:
        import aiohttp
        import tempfile
        song_name = self.action_data.get("song_name", "").strip()
        tts_mode = self.action_data.get("tts_mode", False)
        if isinstance(tts_mode, str):
            tts_mode = tts_mode.lower() == "true"
        if not song_name or song_name == "必填，歌曲名或TTS文本":
            await self.send_text("未输入歌曲名或文本")
            return False, "未输入歌曲名或文本"
        if tts_mode:
            # TTS模式，调用新的API
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    payload = {'text': song_name}
                    async with session.post('http://127.0.0.1:5211/tts', data=payload) as response:
                        if response.status == 200:
                            # Save the returned audio file to a temporary location
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                                temp_audio.write(await response.read())
                                audio_path = temp_audio.name

                            chat_stream = getattr(self, "chat_stream", None)
                            group_id = getattr(getattr(chat_stream, "group_info", None), "group_id", None) if chat_stream else None
                            user_id = getattr(getattr(chat_stream, "user_info", None), "user_id", None) if chat_stream else None
                            from .napcat_client import NapcatClient
                            napcat = NapcatClient()
                            sent = False
                            message_id = None
                            if group_id:
                                success, resp_json = napcat.send_group_record(int(group_id), audio_path)
                                if success:
                                    message_id = resp_json.get("data", {}).get("message_id") if resp_json else None
                                    sent = True
                                from src.plugin_system.apis import generator_api
                                await self.send_text(f"发了")
                                status, rewrite_result, error_message = await generator_api.rewrite_reply(
                                    chat_stream=chat_stream,
                                    reply_data={
                                        "raw_reply": f"TTS语音已发送: {song_name}, 消息ID: {message_id if message_id else '未知'}",
                                        "reason": "tts_mode为True，已发送TTS语音",
                                    },
                                    enable_splitter=False,
                                    enable_chinese_typo=False
                                )
                                if status and rewrite_result:
                                    for reply_seg in rewrite_result:
                                        data = reply_seg[1]
                                        await self.send_text(data)
                                else:
                                    error_msg = error_message if error_message else f"TTS语音已发送: 消息ID: {message_id if message_id else '未知'}"
                                    await self.send_text(error_msg)
                            elif user_id:
                                success, resp_json = napcat.send_private_record(int(user_id), audio_path)
                                if success:
                                    message_id = resp_json.get("data", {}).get("message_id") if resp_json else None
                                    sent = True
                                from src.plugin_system.apis import generator_api
                                status, rewrite_result, error_message = await generator_api.rewrite_reply(
                                    chat_stream=chat_stream,
                                    reply_data={
                                        "raw_reply": f"TTS语音已发送: {song_name}, 消息ID: {message_id if message_id else '未知'}",
                                        "reason": "tts_mode为True，已发送TTS语音",
                                    },
                                    enable_splitter=False,
                                    enable_chinese_typo=False
                                )
                                if status and rewrite_result:
                                    for reply_seg in rewrite_result:
                                        data = reply_seg[1]
                                        await self.send_text(data)
                                else:
                                    error_msg = error_message if error_message else f"TTS语音已发送: 消息ID: {message_id if message_id else '未知'}"
                                    await self.send_text(error_msg)
                            if sent:
                                return True, f"TTS语音已生成并发送: {audio_path}, 消息ID: {message_id if message_id else '未知'}"
                            else:
                                await self.send_text("TTS语音生成成功，但发送失败")
                                return False, "TTS语音生成成功，但发送失败"
                        else:
                            await self.send_text("TTS语音生成失败，API返回错误")
                            return False, "TTS语音生成失败，API返回错误"
            except Exception as e:
                from src.plugin_system.apis import generator_api
                chat_stream = getattr(self, "chat_stream", None)
                result_status, result_message, error_message = await generator_api.rewrite_reply(
                    chat_stream=chat_stream,
                    reply_data={
                        "raw_reply": f"TTS语音生成或发送失败: {e}",
                        "reason": "tts_mode为True，TTS语音生成或发送失败提示润色",
                    }
                )
                if result_status and result_message:
                    for reply_seg in result_message:
                        data = reply_seg[1]
                        await self.send_text(data)
                else:
                    await self.send_text(f"TTS语音生成或发送失败: {e}")
                return False, f"TTS语音生成或发送失败: {e}"
        choose = "1"
        quality = "1"
        # 先请求网易云API获取实际歌名
        api_url = self.get_config("api.base_url", "https://api.vkeys.cn")
        real_song_name = song_name
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "word": song_name,
                    "quality": quality,
                    "choose": choose
                }
                async with session.get(f"{api_url}/v2/music/netease", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == 200 and data.get("data", {}).get("song"):
                            real_song_name = data["data"]["song"]
        except Exception as e:
            pass  # 搜索失败就用原始song_name
        # 处理real_song_name，去除括号及特殊符号，生成safe_real_song_name
        import re
        safe_real_song_name = re.sub(r'[\\/:*?"<>|()（）\[\]{}]', '', real_song_name)
        changed_file = f"{safe_real_song_name}_changed.wav"
        from .msst_separate_tool import find_results_dir
        msst_result_dir = find_results_dir()
        msst_file_path = os.path.join(msst_result_dir, changed_file)
        file_path = None
        if os.path.isfile(msst_file_path):
            file_path = msst_file_path
        elif os.path.isfile(changed_file):
            file_path = changed_file
        sent = False
        message_id = None
        # 检查本地是否已存在
        if file_path and os.path.isfile(file_path):
            chat_stream = getattr(self, "chat_stream", None)
            group_id = getattr(getattr(chat_stream, "group_info", None), "group_id", None) if chat_stream else None
            user_id = getattr(getattr(chat_stream, "user_info", None), "user_id", None) if chat_stream else None
            try:
                from .napcat_client import NapcatClient
                napcat = NapcatClient()
                if group_id:
                    success, resp_json = NapcatClient.send_group_record(int(group_id), file_path)
                    if success:
                        message_id = resp_json.get("data", {}).get("message_id") if resp_json else None
                        sent = True
                    from src.plugin_system.apis import generator_api
                    chat_stream = getattr(self, "chat_stream", None)
                    result_status, result_message = await generator_api.rewrite_reply(
                        chat_stream=chat_stream,
                        reply_data={
                            "raw_reply": f"唱歌已发送: {real_song_name}, 消息ID: {message_id if message_id else '未知'}",
                            "reason": "用户要求唱歌，你已经发送了语音",
                        }
                    )
                    if result_status and result_message:
                        for reply_seg in result_message:
                            data = reply_seg[1]
                            await self.send_text(data)
                    else:
                        await self.send_text(f"已发送: 消息ID: {message_id if message_id else '未知'}")
                elif user_id:
                    success, resp_json = NapcatClient.send_private_record(int(user_id), file_path)
                    if success:
                        message_id = resp_json.get("data", {}).get("message_id") if resp_json else None
                        sent = True
                    from src.plugin_system.apis import generator_api
                    chat_stream = getattr(self, "chat_stream", None)
                    result_status, result_message = await generator_api.rewrite_reply(
                        chat_stream=chat_stream,
                        reply_data={
                            "raw_reply": f"唱歌已发送: {real_song_name}, 消息ID: {message_id if message_id else '未知'}",
                            "reason": "用户要求唱歌，你已经发送了语音",
                        }
                    )
                    if result_status and result_message:
                        for reply_seg in result_message:
                            data = reply_seg[1]
                            await self.send_text(data)
                    else:
                        await self.send_text(f"已发送: 消息ID: {message_id if message_id else '未知'}")
                sent = True
            except Exception as e:
                await self.send_text(f"Napcat语音发送失败: {e}")
        if sent:
            return True, f"本地已存在并已发送: {file_path}"
        # 本地没有则请求生成
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "song": song_name,
                    "choose": choose,
                    "quality": quality
                }
                await session.post("http://127.0.0.1:5211", data=payload)
            # from .generator_tools import generate_rewrite_reply
            chat_stream = getattr(self, "chat_stream", None)
            status, rewrite_result, error_message = await generate_rewrite_reply(
                chat_stream, "收到,已经开始准备", "music_plugin 唤起AI翻唱准备提示润色"
            )
            if status and rewrite_result:
                for reply_seg in rewrite_result:
                    data = reply_seg[1]
                    await self.send_text(data)
            else:
                error_msg = error_message if error_message else "收到,已经开始准备"
                await self.send_text(error_msg)
            return True, "收到,已经开始准备"
        except Exception as e:
            return False, f"处理失败: {e}"

@register_plugin
@register_plugin
class MusicPlugin(BasePlugin):
    """音乐点歌插件
    - 支持网易云音乐点歌、音乐搜索、AI翻唱等功能
    - 支持组件启用控制
    - 支持灵活扩展
    """

    plugin_name = "music_plugin"  # type: ignore
    plugin_description = "网易云音乐点歌插件，支持音乐搜索和点歌功能"  # type: ignore
    plugin_version = "1.0.0"  # type: ignore
    plugin_author = "靓仔"  # type: ignore
    enable_plugin = True  # type: ignore
    config_file_name = "config.toml"  # type: ignore
    dependencies = []  # type: ignore
    python_dependencies = []  # type: ignore

    # 配置节描述
    config_section_descriptions = {
        "plugin": "插件基本配置",
        "components": "组件启用控制",
        "api": "API接口配置", 
        "music": "音乐功能配置",
        "features": "功能开关配置"
    }

    # 配置Schema
    config_schema = {
        "plugin": {
            "enabled": ConfigField(type=bool, default=True, description="是否启用插件")
        },
        "components": {
            "enable_music_search": ConfigField(type=bool, default=True, description="是否启用音乐搜索功能"),
            "enable_music_command": ConfigField(type=bool, default=False, description="是否启用点歌命令功能"),
            "enable_sing_action": ConfigField(type=bool, default=True, description="是否启用AI翻唱/tts功能")
        },
        "api": {
            "base_url": ConfigField(
                type=str, 
                default="https://api.vkeys.cn", 
                description="音乐API基础URL"
            ),
            "timeout": ConfigField(type=int, default=10, description="API请求超时时间(秒)")
        },
        "music": {
            "default_quality": ConfigField(
                type=str, 
                default="9", 
                description="默认音质等级(1-9)"
            ),
            "max_search_results": ConfigField(
                type=int, 
                default=10, 
                description="最大搜索结果数"
            ),
            "msst_result_dir": ConfigField(
                type=str,
                default="D:\so-vits-svc\results",
                description="MSST分离结果目录（AI翻唱/tts语音文件查找目录）"
            )
        },
        "features": {
            "show_cover": ConfigField(type=bool, default=True, description="是否显示专辑封面"),
            "show_download_link": ConfigField(
                type=bool, 
                default=False, 
                description="是否显示下载链接"
            )
        }
    } # type: ignore
    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        """返回插件组件列表，支持按配置启用/禁用组件"""
        components = []
        if self.get_config("components.enable_music_search", True):
            components.append((MusicSearchAction.get_action_info(), MusicSearchAction))
        if self.get_config("components.enable_music_command", False):
            try:
                components.append((MusicCommand.get_command_info(), MusicCommand))
            except Exception:
                pass
        if self.get_config("components.enable_sing_action", True):
            components.append((SingAction.get_action_info(), SingAction))
        # 已移除BilibiliRandomVideoAction相关逻辑
        return components
