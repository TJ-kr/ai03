import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import yaml
from .webdriver_setup import get_chrome_driver, load_config

# 환경 변수 로드 (이미 상위에서 처리됨)

def login_vending_system(driver=None):
    config = load_config()
    website = config['website']
    url = f"https://{website['url']}"
    login_id = os.getenv('VENDING_LOGIN_ID', website['login_id'])
    login_pw = os.getenv('VENDING_LOGIN_PASSWORD', website['login_password'])

    if driver is None:
        driver = get_chrome_driver()

    driver.get(url)
    time.sleep(2)  # 페이지 로딩 대기

    # 로그인 폼 자동 입력 (id, pw 입력란의 name/id/class 속성에 따라 수정 필요)
    # 아래는 예시이며, 실제 HTML 구조에 맞게 수정 필요
    try:
        id_input = driver.find_element(By.NAME, 'id')
    except:
        id_input = driver.find_element(By.ID, 'id')
    id_input.clear()
    id_input.send_keys(login_id)

    try:
        pw_input = driver.find_element(By.NAME, 'pw')
    except:
        pw_input = driver.find_element(By.ID, 'pw')
    pw_input.clear()
    pw_input.send_keys(login_pw)
    pw_input.send_keys(Keys.RETURN)

    time.sleep(3)  # 로그인 처리 대기

    # 로그인 성공 여부 확인 (메인화면의 특정 요소 탐지)
    # 예: '매출현황' 텍스트, 또는 특정 대시보드 요소
    page_source = driver.page_source
    if '매출현황' in page_source or '메인화면' in page_source:
        print('로그인 성공!')
        return driver
    else:
        print('로그인 실패!')
        driver.quit()
        return None

if __name__ == "__main__":
    driver = login_vending_system()
    if driver:
        print('테스트용: 5초 후 브라우저 종료')
        time.sleep(5)
        driver.quit() 