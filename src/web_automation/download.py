import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .login import login_vending_system
from ..utils.logger import get_logger
from ..utils.error_handler import safe_action
from ..web_automation.webdriver_setup import load_config

# 로그 함수 (간단 버전)
def log(msg):
    print(f"[DOWNLOAD] {msg}")

def download_sales_excel(driver=None):
    config = load_config()
    download_folder = config['data_processing']['download_folder']
    os.makedirs(download_folder, exist_ok=True)

    if driver is None:
        driver = login_vending_system()
        if driver is None:
            log('로그인 실패로 다운로드 중단')
            return False

    # 다운로드 버튼 탐색 (예시: 버튼 텍스트, id, class 등 실제 구조에 맞게 수정 필요)
    try:
        # 예시: '엑셀' 또는 '다운로드' 텍스트가 있는 버튼
        download_btn = driver.find_element(By.XPATH, "//button[contains(text(), '엑셀') or contains(text(), '다운로드')]")
        ActionChains(driver).move_to_element(download_btn).click().perform()
        log('엑셀 다운로드 버튼 클릭')
    except Exception as e:
        log(f'다운로드 버튼 탐색 실패: {e}')
        driver.quit()
        return False

    # 다운로드 완료 대기 (최대 30초)
    filename = None
    for _ in range(30):
        files = os.listdir(download_folder)
        excel_files = [f for f in files if f.endswith('.xls') or f.endswith('.xlsx')]
        if excel_files:
            filename = excel_files[0]
            log(f'다운로드 완료: {filename}')
            break
        time.sleep(1)
    else:
        log('다운로드 파일을 찾지 못함')
        driver.quit()
        return False

    # 필요시 파일명 변경 등 추가 처리
    driver.quit()
    return os.path.join(download_folder, filename)

if __name__ == "__main__":
    result = download_sales_excel()
    if result:
        print(f'엑셀 파일 다운로드 성공: {result}')
    else:
        print('엑셀 파일 다운로드 실패') 