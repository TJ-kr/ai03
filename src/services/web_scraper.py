import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ..config.settings import Settings
from ..utils.logger import get_logger
from ..utils.helpers import ensure_directory, get_latest_file

class WebScraper:
    def __init__(self):
        self.logger = get_logger()
        self.driver = None
        self.download_dir = os.path.abspath(Settings.DOWNLOAD_DIR)
        ensure_directory(self.download_dir)
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()
        # 헤드리스 모드 (브라우저 창이 뜨지 않음)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 다운로드 경로 설정
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.logger.info("Chrome 드라이버 초기화 완료")
        except Exception as e:
            self.logger.error(f"Chrome 드라이버 초기화 실패: {str(e)}")
            raise
    
    def login(self):
        """TOYGO 웹사이트 로그인"""
        try:
            self.logger.info(f"TOYGO 웹사이트 로그인 시작: {Settings.WEBSITE_URL}")
            self.driver.get(Settings.WEBSITE_URL)
            
            # 페이지 로딩 대기
            wait = WebDriverWait(self.driver, 10)
            
            # 로그인 폼이 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.NAME, "email")))
            
            # 아이디 입력
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.clear()
            email_field.send_keys(Settings.WEBSITE_USERNAME)
            self.logger.info("아이디 입력 완료")
            
            # 비밀번호 입력
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(Settings.WEBSITE_PASSWORD)
            self.logger.info("비밀번호 입력 완료")
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.ID, "btn-sign-in")
            login_button.click()
            self.logger.info("로그인 버튼 클릭")
            
            # 로그인 성공 확인 (대시보드 페이지로 이동했는지 확인)
            try:
                # 로그인 후 대시보드 페이지의 특정 요소가 나타날 때까지 대기
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                
                # 현재 URL 확인
                current_url = self.driver.current_url
                if "apply/index.php" in current_url or "dashboard" in current_url:
                    self.logger.info("로그인 성공 - 대시보드 페이지로 이동")
                else:
                    self.logger.info(f"로그인 성공 - 현재 페이지: {current_url}")
                
            except TimeoutException:
                # 로그인 에러 메시지 확인
                try:
                    error_element = self.driver.find_element(By.ID, "login_error_info")
                    error_text = error_element.text
                    if error_text:
                        raise Exception(f"로그인 실패: {error_text}")
                except NoSuchElementException:
                    pass
                
                # 에러 메시지가 없어도 로그인 실패로 간주
                raise Exception("로그인 후 대시보드 페이지로 이동하지 못했습니다")
            
        except Exception as e:
            self.logger.error(f"로그인 실패: {str(e)}")
            # 스크린샷 저장 (디버깅용)
            try:
                screenshot_path = os.path.join(self.download_dir, f"login_error_{int(time.time())}.png")
                self.driver.save_screenshot(screenshot_path)
                self.logger.info(f"로그인 에러 스크린샷 저장: {screenshot_path}")
            except:
                pass
            raise
    
    def navigate_to_sales_management(self):
        """매출 관리 페이지로 이동"""
        try:
            self.logger.info("매출 관리 페이지로 이동 시작")
            wait = WebDriverWait(self.driver, 10)
            
            # 매출 관리 버튼 찾기 및 클릭
            sales_management_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/payment/index.php') and contains(text(), '매출 관리')]"))
            )
            sales_management_link.click()
            self.logger.info("매출 관리 버튼 클릭")
            
            # 페이지 로딩 대기
            time.sleep(3)
            
        except Exception as e:
            self.logger.error(f"매출 관리 페이지 이동 실패: {str(e)}")
            raise
    
    def select_distributor(self):
        """총판 선택 - 로컬러 선택"""
        try:
            self.logger.info("총판 선택 시작")
            wait = WebDriverWait(self.driver, 10)
            
            # 총판 드롭다운 찾기
            distributor_select = wait.until(
                EC.presence_of_element_located((By.ID, "group_first"))
            )
            
            # Select 객체 생성
            select = Select(distributor_select)
            
            # 로컬러 선택 (value="040")
            select.select_by_value("040")
            self.logger.info("로컬러 선택 완료")
            
            time.sleep(2)  # 선택 후 대기
            
        except Exception as e:
            self.logger.error(f"총판 선택 실패: {str(e)}")
            raise
    
    def set_date_range(self, start_date=None, end_date=None):
        """조회 기간 설정"""
        try:
            self.logger.info("조회 기간 설정 시작")
            wait = WebDriverWait(self.driver, 10)
            
            # 기본값: 어제 날짜
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if end_date is None:
                end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            # 시작일 입력
            start_date_input = wait.until(
                EC.presence_of_element_located((By.ID, "dash-date1"))
            )
            start_date_input.clear()
            start_date_input.send_keys(start_date)
            self.logger.info(f"시작일 설정: {start_date}")
            
            # 종료일 입력
            end_date_input = self.driver.find_element(By.ID, "dash-date2")
            end_date_input.clear()
            end_date_input.send_keys(end_date)
            self.logger.info(f"종료일 설정: {end_date}")
            
            time.sleep(1)  # 입력 후 대기
            
        except Exception as e:
            self.logger.error(f"조회 기간 설정 실패: {str(e)}")
            raise
    
    def click_search_button(self):
        """검색 버튼 클릭"""
        try:
            self.logger.info("검색 버튼 클릭 시작")
            wait = WebDriverWait(self.driver, 10)
            
            # 검색 버튼 찾기 및 클릭
            search_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'searchTotal()')]"))
            )
            search_button.click()
            self.logger.info("검색 버튼 클릭")
            
            # 검색 결과 로딩 대기
            time.sleep(5)
            
        except Exception as e:
            self.logger.error(f"검색 버튼 클릭 실패: {str(e)}")
            raise
    
    def download_excel_file(self):
        """Excel 파일 다운로드"""
        try:
            self.logger.info("Excel 파일 다운로드 시작")
            wait = WebDriverWait(self.driver, 10)
            
            # 다운로드 전 파일 목록 저장
            before_files = set(os.listdir(self.download_dir))
            
            # 다운로드 아이콘 찾기 및 클릭
            download_icon = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'fa-download')]"))
            )
            download_icon.click()
            self.logger.info("다운로드 아이콘 클릭")
            
            time.sleep(2)
            
            # Excel 드롭다운 메뉴 찾기 및 클릭
            excel_menu = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'fa-file-text')]"))
            )
            excel_menu.click()
            self.logger.info("Excel 메뉴 클릭")
            
            # 다운로드 완료 대기
            time.sleep(10)
            
            # 다운로드 후 파일 목록 확인
            after_files = set(os.listdir(self.download_dir))
            new_files = after_files - before_files
            
            if new_files:
                downloaded_file = os.path.join(self.download_dir, list(new_files)[0])
                self.logger.info(f"Excel 파일 다운로드 완료: {downloaded_file}")
                return downloaded_file
            else:
                raise Exception("다운로드된 Excel 파일을 찾을 수 없습니다")
                
        except Exception as e:
            self.logger.error(f"Excel 파일 다운로드 실패: {str(e)}")
            raise
    
    def download_file(self, download_url=None, start_date=None, end_date=None):
        """전체 다운로드 프로세스 실행"""
        try:
            self.logger.info("매출 데이터 다운로드 프로세스 시작")
            
            # 1. 매출 관리 페이지로 이동
            self.navigate_to_sales_management()
            
            # 2. 총판 선택 (로컬러)
            self.select_distributor()
            
            # 3. 조회 기간 설정
            self.set_date_range(start_date, end_date)
            
            # 4. 검색 버튼 클릭
            self.click_search_button()
            
            # 5. Excel 파일 다운로드
            downloaded_file = self.download_excel_file()
            
            return downloaded_file
            
        except Exception as e:
            self.logger.error(f"다운로드 프로세스 실패: {str(e)}")
            raise
    
    def get_latest_downloaded_file(self):
        """가장 최근 다운로드된 파일 반환"""
        return get_latest_file(self.download_dir)
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Chrome 드라이버 종료")
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.close() 