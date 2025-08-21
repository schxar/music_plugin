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
    # 优先检查是否已存在处理结果
    base_name = os.path.splitext(os.path.basename(input_wav))[0]
    changed_path = os.path.join(os.path.dirname(input_wav), f"{base_name}_changed.wav")
    if os.path.exists(changed_path):
        return changed_path
    driver = webdriver.Chrome()
    driver.get(gradio_url)
    wait = WebDriverWait(driver, 20)
    # 刷新选项
    refresh_button = wait.until(EC.element_to_be_clickable((By.ID, "component-20")))
    refresh_button.click()
    time.sleep(1)
    # 选择模型
    model_select_span = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-6 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    )
    model_select_span.click()
    time.sleep(1)
    options = driver.find_elements(By.CSS_SELECTOR, "ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    for option in options:
        label = option.get_attribute("aria-label") or option.text
        if label.strip() == "jo.pth":
            option.click()
            break
    time.sleep(1)
    # # 选择扩散模型
    # diffusion_span = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#component-15 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    # )
    # diffusion_span.click()
    # time.sleep(1)
    # diff_options = driver.find_elements(By.CSS_SELECTOR, "#component-15 ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    # for option in diff_options:
    #     label = option.get_attribute("aria-label") or option.text
    #     if label.strip() == "anon.pt":
    #         option.click()
    #         break
    # time.sleep(2)
    #
    # # 选择扩散模型配置文件 diffusion.yaml
    # config_span = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#component-16 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    # )
    # config_span.click()
    # time.sleep(1)
    # config_options = driver.find_elements(By.CSS_SELECTOR, "#component-16 ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    # for option in config_options:
    #     label = option.get_attribute("aria-label") or option.text
    #     if label.strip() == "diffusion.yaml":
    #         option.click()
    #         break
    # time.sleep(1)
    
    
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
        # 优先查找所有audio标签，找src属性包含_vocals_qingxu_ 或 _sovdiff_ 的wav
        for _ in range(60):
            audio_elems = driver.find_elements(By.TAG_NAME, "audio")
            for audio_elem in audio_elems:
                src = audio_elem.get_attribute("src")
                if src and ("_vocals_qingxu_" in src or src.endswith(".wav") or "_sovdiff_" in src):
                    audio_src = src
                    break
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
        # 如果src是file=本地路径，直接复制本地文件
        if audio_src.startswith("http://") and "file=" in audio_src:
            import urllib.parse
            local_path = audio_src.split("file=")[-1]
            local_path = urllib.parse.unquote(local_path)
            if os.path.exists(local_path):
                import shutil
                shutil.copy(local_path, output_path)
            else:
                # 兜底用requests下载
                with requests.get(audio_src, stream=True) as r:
                    r.raise_for_status()
                    with open(output_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
        else:
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

def gradio_process_vocal_tts(text: str, gradio_url: str = "http://127.0.0.1:7860") -> str:
    """
    用Selenium自动在Gradio页面进行文字转语音，返回处理后wav路径。
    :param text: 输入的文本内容
    :param gradio_url: Gradio WebUI地址
    :return: 处理后wav文件路径
    """
    import shutil
    driver = webdriver.Chrome()
    driver.get(gradio_url)
    wait = WebDriverWait(driver, 20)
    # 刷新选项
    refresh_button = wait.until(EC.element_to_be_clickable((By.ID, "component-20")))
    refresh_button.click()
    time.sleep(1)
    # 选择模型
    model_select_span = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-6 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    )
    model_select_span.click()
    time.sleep(1)
    options = driver.find_elements(By.CSS_SELECTOR, "ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    for option in options:
        label = option.get_attribute("aria-label") or option.text
        if label.strip() == "jo.pth":
            option.click()
            break
    time.sleep(1)
    # # 选择扩散模型
    # diffusion_span = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#component-15 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    # )
    # diffusion_span.click()
    # time.sleep(1)
    # diff_options = driver.find_elements(By.CSS_SELECTOR, "#component-15 ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    # for option in diff_options:
    #     label = option.get_attribute("aria-label") or option.text
    #     if label.strip() == "anon.pt":
    #         option.click()
    #         break
    # time.sleep(2)
    # # 选择扩散模型配置文件 diffusion.yaml
    # config_span = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#component-16 > label > div > div.wrap-inner.svelte-1ythexu > span"))
    # )
    # config_span.click()
    # time.sleep(1)
    # config_options = driver.find_elements(By.CSS_SELECTOR, "#component-16 ul.options.svelte-1oas11n > li.item.svelte-1oas11n")
    # for option in config_options:
    #     label = option.get_attribute("aria-label") or option.text
    #     if label.strip() == "diffusion.yaml":
    #         option.click()
    #         break
    # time.sleep(1)
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
    # 点击“文字转语音”按钮（如果未选中才点击）
    tts_tab_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '文字转语音')]"))
    )
    # 检查是否已选中
    btn_class = tts_tab_btn.get_attribute('class') or ''
    if 'selected' not in btn_class:
        tts_tab_btn.click()
        time.sleep(1)
    # 选择说话人性别为“女”
    female_radio = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-49 input[type='radio'][value='女']"))
    )
    if not female_radio.is_selected():
        female_radio.click()
        time.sleep(0.5)
    # 输入文本到textarea（限定component-47下）
    textarea = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#component-47 textarea[data-testid='textbox']"))
    )
    textarea.clear()
    textarea.send_keys(text)
    time.sleep(1)
    # 点击“文本转语音”按钮
    tts_submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "component-85"))
    )
    tts_submit_btn.click()
    time.sleep(10)
    # 查找音频输出audio标签，获取src并下载
    from selenium.common.exceptions import TimeoutException
    audio_src = None
    try:
        for _ in range(60):
            audio_elems = driver.find_elements(By.TAG_NAME, "audio")
            for audio_elem in audio_elems:
                src = audio_elem.get_attribute("src")
                if src and (src.endswith(".wav") or "_tts_" in src):
                    audio_src = src
                    break
            if audio_src:
                break
            time.sleep(1)
        if not audio_src:
            raise RuntimeError("未能获取到音频输出的src属性！")
    except TimeoutException as e:
        screenshot_path = os.path.join(os.getcwd(), 'gradio_tts_debug_screenshot.png')
        driver.save_screenshot(screenshot_path)
        print(f"[错误] 等待audio标签超时，已保存页面截图: {screenshot_path}")
        driver.quit()
        raise RuntimeError(f"等待audio标签超时: {e}")
    except Exception as e:
        screenshot_path = os.path.join(os.getcwd(), 'gradio_tts_debug_screenshot.png')
        driver.save_screenshot(screenshot_path)
        print(f"[错误] 获取audio标签异常，已保存页面截图: {screenshot_path}")
        driver.quit()
        raise
    # 用audio_src里的文件名作为输出名
    import requests
    import urllib.parse
    from urllib.parse import urlparse
    output_dir = os.getcwd()
    # 提取文件名
    parsed_url = urlparse(audio_src)
    if 'file=' in audio_src:
        # 兼容file=参数
        file_part = audio_src.split('file=')[-1]
        file_part = urllib.parse.unquote(file_part)
        output_name = os.path.basename(file_part)
    else:
        output_name = os.path.basename(parsed_url.path)
    output_path = os.path.join(output_dir, output_name)
    try:
        if audio_src.startswith("http://") and "file=" in audio_src:
            local_path = audio_src.split("file=")[-1]
            local_path = urllib.parse.unquote(local_path)
            if os.path.exists(local_path):
                import shutil
                shutil.copy(local_path, output_path)
            else:
                with requests.get(audio_src, stream=True) as r:
                    r.raise_for_status()
                    with open(output_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
        else:
            with requests.get(audio_src, stream=True) as r:
                r.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        # 下载成功后卸载模型
        try:
            unload_button = driver.find_element(By.ID, "component-32")
            unload_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"[警告] 退出前卸载模型失败: {e}")
    except Exception as e:
        print(f"[错误] 下载音频失败: {e}")
        driver.quit()
        raise
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
