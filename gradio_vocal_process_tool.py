import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def gradio_process_vocal(input_wav: str, gradio_url: str = "http://127.0.0.1:7860") -> str:
    """
    用Selenium自动上传vocal wav到Gradio并处理，返回处理后wav路径。
    :param input_wav: 输入的vocal wav文件路径
    :param gradio_url: Gradio WebUI地址
    :return: 处理后wav文件路径
    """
    if not os.path.exists(input_wav):
        raise FileNotFoundError(f"输入wav不存在: {input_wav}")
    driver = webdriver.Chrome()
    driver.get(gradio_url)
    wait = WebDriverWait(driver, 20)

    # 选择模型
    model_select_span = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-6 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    )
    model_select_span.click()
    time.sleep(1)
    options = driver.find_elements(By.CSS_SELECTOR, "ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    for option in options:
        label = option.get_attribute("aria-label") or option.text
        if label.strip() == "G_43900.pth":
            option.click()
            break
    time.sleep(1)
    # 选择扩散模型
    diffusion_span = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-15 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    )
    diffusion_span.click()
    time.sleep(1)
    diff_options = driver.find_elements(By.CSS_SELECTOR, "#component-15 ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    for option in diff_options:
        label = option.get_attribute("aria-label") or option.text
        if label.strip() == "model_30000.pt":
            option.click()
            break
    time.sleep(2)
    # 卸载模型
    unload_button = wait.until(
        EC.element_to_be_clickable((By.ID, "component-32"))
    )
    unload_button.click()
    time.sleep(2)
    # 加载模型
    load_button = wait.until(
        EC.element_to_be_clickable((By.ID, "component-31"))
    )
    load_button.click()
    time.sleep(5)
    # 上传vocal wav
    vc_input3 = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-40 input[type='file']"))
    )
    vc_input3.send_keys(input_wav)
    time.sleep(1)
    # 点击音频转换按钮
    vc_submit_button = wait.until(
        EC.element_to_be_clickable((By.ID, "component-83"))
    )
    vc_submit_button.click()
    time.sleep(30)
    # 查找音频输出audio标签，获取src并下载
    from selenium.common.exceptions import TimeoutException
    audio_src = None
    try:
        # 优先用原选择器，找不到则尝试更通用的audio标签
        try:
            audio_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "audio.svelte-eemfgq"))
            )
        except TimeoutException:
            print("[调试] 未找到 audio.svelte-eemfgq，尝试查找任意audio标签……")
            audio_elem = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "audio"))
            )
        for _ in range(60):
            audio_src = audio_elem.get_attribute("src")
            if audio_src:
                break
            time.sleep(1)
        if not audio_src:
            raise RuntimeError("未能获取到音频输出的src属性！")
    except TimeoutException as e:
        # 保存页面截图，便于排查
        screenshot_path = os.path.join(os.path.dirname(input_wav), 'gradio_debug_screenshot.png')
        driver.save_screenshot(screenshot_path)
        print(f"[错误] 等待audio标签超时，已保存页面截图: {screenshot_path}")
        # 退出前再次尝试卸载模型
        try:
            unload_button = driver.find_element(By.ID, "component-32")
            unload_button.click()
            time.sleep(2)
        except Exception as e2:
            print(f"[警告] 退出前卸载模型失败: {e2}")
        driver.quit()
        raise RuntimeError(f"等待audio标签超时: {e}")
    except Exception as e:
        screenshot_path = os.path.join(os.path.dirname(input_wav), 'gradio_debug_screenshot.png')
        driver.save_screenshot(screenshot_path)
        print(f"[错误] 获取audio标签异常，已保存页面截图: {screenshot_path}")
        # 退出前再次尝试卸载模型
        try:
            unload_button = driver.find_element(By.ID, "component-32")
            unload_button.click()
            time.sleep(2)
        except Exception as e2:
            print(f"[警告] 退出前卸载模型失败: {e2}")
        driver.quit()
        raise
    # 下载输出wav
    output_path = os.path.join(os.path.dirname(input_wav), 'gradio_output.wav')
    import requests
    try:
        with requests.get(audio_src, stream=True) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"[错误] 下载音频失败: {e}")
        # 退出前再次尝试卸载模型
        try:
            unload_button = driver.find_element(By.ID, "component-32")
            unload_button.click()
            time.sleep(2)
        except Exception as e2:
            print(f"[警告] 退出前卸载模型失败: {e2}")
        driver.quit()
        raise
    # 处理完成后正常退出前也卸载模型
    try:
        unload_button = driver.find_element(By.ID, "component-32")
        unload_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"[警告] 退出前卸载模型失败: {e}")
    driver.quit()
    return output_path

if __name__ == "__main__":
    # 示例用法
    test_wav = os.path.join(os.path.dirname(__file__), 'cache', 'test_vocals.wav')
    try:
        out_wav = gradio_process_vocal(test_wav)
        print(f"Gradio处理完成: {out_wav}")
    except Exception as e:
        print(f"处理失败: {e}")
