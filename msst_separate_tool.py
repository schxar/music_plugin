import os
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_results_dir():
    """
    从当前目录开始，递归向上查找 MSST-WebUI-zluda/results 文件夹。
    找到后返回其绝对路径，否则抛出异常。
    """
    cur = os.path.abspath(os.getcwd())
    while True:
        candidate = os.path.join(cur, 'MSST-WebUI-zluda', 'results')
        if os.path.isdir(candidate):
            return candidate
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    raise FileNotFoundError("未找到 MSST-WebUI-zluda/results 目录，请检查目录结构！")

def msst_separate(flac_path: str, results_dir: Optional[str] = None, webui_url: str = "http://127.0.0.1:7861"):
    """
    使用MSST-WebUI自动分离flac音频，返回分离后other和vocals的wav路径。
    :param flac_path: 输入的flac文件路径
    :param results_dir: 结果目录，默认在MSST-WebUI-zluda/results下
    :param webui_url: MSST-WebUI地址
    :return: (other_wav_path, vocals_wav_path)
    """
    if not os.path.exists(flac_path):
        raise FileNotFoundError(f"音频文件不存在: {flac_path}")
    if results_dir is None:
        results_dir = find_results_dir()
    base_name = os.path.splitext(os.path.basename(flac_path))[0]
    other_path = os.path.join(results_dir, f'{base_name}_other.wav')
    vocals_path = os.path.join(results_dir, f'{base_name}_vocals.wav')
    # 如果分离结果已存在，直接返回
    if os.path.exists(other_path) and os.path.exists(vocals_path):
        return other_path, vocals_path
    # 启动浏览器
    driver = webdriver.Chrome()
    driver.get(webui_url)
    wait = WebDriverWait(driver, 20)

    # # 1. 勾选显卡
    # gpu_checkbox = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='0: NVIDIA GeForce RTX 4060 Laptop GPU']"))
    # )
    # gpu_checkbox.click()
    # time.sleep(1)
    # # 2. 勾选vocals
    # vocals_checkbox = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='vocals']"))
    # )
    # vocals_checkbox.click()
    # time.sleep(1)
    # # 3. 勾选other
    # other_checkbox = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='other']"))
    # )
    # other_checkbox.click()
    # time.sleep(1)
    # 4. 上传flac
    file_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][data-testid='file-upload']"))
    )
    file_input.send_keys(flac_path)
    time.sleep(8)  # 等待上传
    # 5. 点击分离按钮
    split_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "component-47"))
    )
    split_btn.click()
    # 6. 检测 Output Message 文本框内容，判断分离是否完成
    timeout = 300  # 最长等待5分钟
    interval = 4   # 每4秒检查一次
    waited = 0
    finished = False
    while waited < timeout:
        try:
            output_label = driver.find_element(By.XPATH, "//span[@data-testid='block-info' and contains(text(), 'Output Message')]/following-sibling::textarea")
            msg = output_label.get_attribute('value') or output_label.text or output_label.get_attribute('innerText')
            if msg and ("完成" in msg or "success" in msg.lower() or "分离完成" in msg):
                finished = True
                break
            # 检查分离后的文件是否存在
            if os.path.exists(other_path) and os.path.exists(vocals_path):
                finished = True
                break
        except Exception:
            pass
        time.sleep(interval)
        waited += interval
    if not finished:
        driver.quit()
        raise TimeoutError("等待分离Output Message超时或文件未生成！")
    driver.quit()
    return other_path, vocals_path

if __name__ == "__main__":
    # 示例用法
    flac_file = os.path.join(os.path.dirname(__file__), 'cache', 'test.flac')
    try:
        other, vocals = msst_separate(flac_file)
        print(f"分离完成:\nother: {other}\nvocals: {vocals}")
    except Exception as e:
        print(f"分离失败: {e}")
