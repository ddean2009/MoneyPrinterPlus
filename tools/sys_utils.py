import psutil


def is_chrome_running():
    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        # 检查进程名是否包含chrome
        if 'chrome' in proc.info['name'].lower():
            return True
    return False


def is_firefox_running():
    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        # 检查进程名是否包含chrome
        if 'firefox' in proc.info['name'].lower():
            return True
    return False
