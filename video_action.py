import asyncio
import random
import traceback
from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from src.chat.actions.plugin_action import PluginAction, register_action
from src.chat.actions.base_action import ActionActivationType, ChatMode
from src.common.logger_manager import get_logger

logger = get_logger("video_action")

@register_action
class VideoAction(PluginAction):
    """获取B站视频信息的动作处理类"""

    action_name = "video_action"
    action_description = "获取B站视频信息并随机选择一个视频"
    action_parameters = {}
    action_require = [
        "当用户要求来首歌时使用",
        "当需要随机获取B站视频时使用"
    ]
    enable_plugin = False
    
    focus_activation_type = ActionActivationType.LLM_JUDGE
    normal_activation_type = ActionActivationType.KEYWORD
    
    activation_keywords = ["来首歌"]
    keyword_case_sensitive = False
    
    llm_judge_prompt = """
判定是否需要使用视频动作的条件：
1. 用户明确要求"来首歌"
2. 用户想要随机获取一个B站视频
3. 用户想要听音乐或看视频

适合使用的情况：
- "来首歌"
- "随机播放一个视频"
- "给我推荐个视频"

绝对不要使用的情况：
1. 纯文字聊天
2. 谈论已存在的视频
3. 用户明确表示不需要视频时
"""
    
    mode_enable = ChatMode.ALL
    parallel_action = True

    def __init__(self, action_data, reasoning, cycle_timers, thinking_id, global_config=None, **kwargs):
        super().__init__(action_data, reasoning, cycle_timers, thinking_id, global_config, **kwargs)
        logger.info(f"{self.log_prefix} 初始化视频动作")

    async def process(self) -> Tuple[bool, str]:
        """处理视频获取请求"""
        logger.info(f"{self.log_prefix} 执行 video_action")
        
        await self.send_message_by_expressor("正在为您随机挑选一首歌，请稍候...")
        
        try:
            # 设置Selenium选项
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            try:
                # 指定ChromeDriver路径
                service = Service(executable_path="chromedriver")
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except WebDriverException as e:
                logger.error(f"{self.log_prefix} ChromeDriver初始化失败: {str(e)}")
                await self.send_message_by_expressor("视频服务初始化失败，请检查ChromeDriver配置")
                return False, f"ChromeDriver初始化失败: {str(e)}"
            driver.get("https://space.bilibili.com/488978908/upload/video")
            
            try:
                # 等待视频卡片加载
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".upload-video-card"))
                )
                
                # 获取所有视频卡片
                video_cards = driver.find_elements(By.CSS_SELECTOR, ".upload-video-card .bili-video-card")
                
                if not video_cards:
                    await self.send_message_by_expressor("没有找到可用的视频")
                    return False, "没有找到视频卡片"
                    
            except TimeoutException:
                logger.error(f"{self.log_prefix} 等待视频卡片加载超时")
                await self.send_message_by_expressor("加载视频列表超时，请稍后再试")
                return False, "加载视频列表超时"
            
            # 随机选择一个视频
            selected_video = random.choice(video_cards)
            
            # 提取视频信息
            title = selected_video.find_element(By.CSS_SELECTOR, ".bili-video-card__title").text
            url = selected_video.find_element(By.CSS_SELECTOR, ".bili-cover-card").get_attribute("href")
            
            # 关闭浏览器
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"{self.log_prefix} 关闭浏览器时出错: {str(e)}")
            
            # 发送结果
            message = f"🎵 为您推荐: {title}\n🔗 视频链接: {url}"
            await self.send_message(type="text", data=message)
            
            return True, "视频获取成功"
            
        except Exception as e:
            logger.error(f"{self.log_prefix} 获取视频时出错: {traceback.format_exc()}")
            await self.send_message_by_expressor("获取视频时出错了，请稍后再试")
            return False, f"视频获取失败: {str(e)}"

