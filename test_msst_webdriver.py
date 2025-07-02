from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 启动浏览器并打开本地7861端口
url = "http://127.0.0.1:7861"
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 20)

# 1. 勾选显卡复选框（假设只有一个显卡，名称为0: NVIDIA GeForce RTX 4060 Laptop GPU）
#gpu_checkbox = wait.until(
##    EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='0: NVIDIA GeForce RTX 4060 Laptop GPU']"))
#)
#gpu_checkbox.click()
time.sleep(1)

# 2. 勾选vocals复选框
#vocals_checkbox = wait.until(
#    EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='vocals']"))
#)
#vocals_checkbox.click()
time.sleep(1)

# 3. 勾选other复选框
##other_checkbox = wait.until(
#    EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='other']"))
#)
#other_checkbox.click()
time.sleep(1)


# 4. 拖拽上传网易云音乐音频文件
import os
from selenium.webdriver.common.action_chains import ActionChains


# 假设音频文件路径为cache/test.flac
audio_path = os.path.join(os.path.dirname(__file__), 'cache', 'test.flac')
if not os.path.exists(audio_path):
    print(f"音频文件不存在: {audio_path}")
else:
    # 找到上传按钮的input[type='file']
    file_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][data-testid='file-upload']"))
    )

    # 直接用send_keys上传文件
    file_input.send_keys(audio_path)
    time.sleep(8)  # 等待8秒，确保文件上传完成
    print(f"已上传音频文件: {audio_path}")

    # 5. 点击“输入音频分离”按钮
    split_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "component-47"))
    )
    split_btn.click()
    print("已点击‘输入音频分离’按钮，等待分离结果...")

    # 6. 等待 results 目录下出现新的 test_other.wav 和 test_vocals.wav
    import pathlib
    results_dir = os.path.join(os.path.dirname(__file__), 'MSST-WebUI-zluda', 'results')
    other_path = os.path.join(results_dir, 'test_other.wav')
    vocals_path = os.path.join(results_dir, 'test_vocals.wav')
    timeout = 180  # 最长等待2分钟
    interval = 2
    waited = 0
    while waited < timeout:
        if os.path.exists(other_path) and os.path.exists(vocals_path):
            print(f"分离完成: {other_path}, {vocals_path}")
            break
        time.sleep(interval)
        waited += interval
    else:
        print("等待分离结果超时！")

print("全部复选框已点击完成并上传音频！")
# 保持浏览器窗口不退出，便于后续人工检查
input("操作已完成，按回车键关闭浏览器...")
driver.quit()
