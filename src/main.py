#!/usr/bin/env python3
"""
자판기 매출 관리 시스템 메인 실행 파일
"""

import argparse
import schedule
import time
import sys
import os
from datetime import datetime
from jinja2 import Template

# 프로젝트 루트 경로를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings
from utils.logger import setup_logger, get_logger
from utils.helpers import ensure_directory
from services.web_scraper import WebScraper
from services.spreadsheet_handler import SpreadsheetHandler
from services.data_processor import DataProcessor
from services.email_sender import EmailSender

class VendingMachineAutomation:
    def __init__(self):
        self.logger = get_logger()
        self.spreadsheet_handler = None
        self.data_processor = None
        self.email_sender = None
    
    def setup(self):
        """시스템 초기 설정"""
        try:
            # 설정 검증
            Settings.validate_settings()
            
            # 필요한 디렉토리 생성
            ensure_directory(Settings.DOWNLOAD_DIR)
            ensure_directory(Settings.LOGS_DIR)
            
            # 서비스 초기화
            self.spreadsheet_handler = SpreadsheetHandler()
            self.data_processor = DataProcessor()
            self.email_sender = EmailSender()
            
            # 스프레드시트 열기
            self.spreadsheet_handler.open_spreadsheet()
            
            self.logger.info("시스템 초기화 완료")
            return True
            
        except Exception as e:
            self.logger.error(f"시스템 초기화 실패: {str(e)}")
            return False
    
    def run_automation(self):
        """자동화 프로세스 실행"""
        try:
            self.logger.info("자동화 프로세스 시작")
            
            # 1. 웹사이트에서 파일 다운로드
            downloaded_file = self._download_file()
            if not downloaded_file:
                self.logger.error("파일 다운로드 실패")
                return False
            
            # 2. 다운로드된 파일 처리
            processed_data = self._process_file(downloaded_file)
            if not processed_data:
                self.logger.error("파일 처리 실패")
                return False
            
            # 3. 스프레드시트에 데이터 추가
            success = self._update_spreadsheet(processed_data['spreadsheet_data'])
            if not success:
                self.logger.warning("스프레드시트 업데이트 실패 또는 중복 데이터")
            
            # 4. 이메일 보고서 생성 및 발송
            self._send_email_report(processed_data['summary'])
            
            self.logger.info("자동화 프로세스 완료")
            return True
            
        except Exception as e:
            self.logger.error(f"자동화 프로세스 실패: {str(e)}")
            return False
    
    def _download_file(self):
        """파일 다운로드"""
        try:
            with WebScraper() as scraper:
                scraper.login()
                downloaded_file = scraper.download_file()
                return downloaded_file
        except Exception as e:
            self.logger.error(f"파일 다운로드 실패: {str(e)}")
            return None
    
    def _process_file(self, file_path):
        """파일 처리"""
        try:
            return self.data_processor.process_downloaded_file(file_path)
        except Exception as e:
            self.logger.error(f"파일 처리 실패: {str(e)}")
            return None
    
    def _update_spreadsheet(self, data):
        """스프레드시트 업데이트"""
        try:
            # 헤더를 제외한 데이터만 추가
            if len(data) > 1:
                for row in data[1:]:  # 헤더 제외
                    success = self.spreadsheet_handler.append_to_main_sheet(row)
                    if not success:
                        self.logger.warning("중복 데이터로 인해 추가하지 않음")
            return True
        except Exception as e:
            self.logger.error(f"스프레드시트 업데이트 실패: {str(e)}")
            return False
    
    def _send_email_report(self, summary_data):
        """이메일 보고서 발송"""
        try:
            # 스프레드시트에서 데이터 가져오기
            table1_data = self.spreadsheet_handler.get_table1_data()
            table2_data = self.spreadsheet_handler.get_table2_monthly_data()
            
            # 이메일 내용 생성
            email_content = self.data_processor.create_email_content(
                summary_data, table1_data, table2_data
            )
            
            # HTML 이메일 생성
            html_content = self._create_html_email(
                summary_data, table1_data, table2_data
            )
            
            # 이메일 발송
            self.email_sender.send_email(
                Settings.EMAIL_SUBJECT,
                email_content
            )
            
            # HTML 이메일도 발송 (선택사항)
            # self.email_sender.send_html_email(
            #     Settings.EMAIL_SUBJECT,
            #     html_content
            # )
            
            self.logger.info("이메일 보고서 발송 완료")
            
        except Exception as e:
            self.logger.error(f"이메일 보고서 발송 실패: {str(e)}")
    
    def _create_html_email(self, summary_data, table1_data, table2_data):
        """HTML 이메일 생성"""
        try:
            # HTML 템플릿 읽기
            template_path = os.path.join(
                os.path.dirname(__file__), 
                'templates', 
                'email_template.html'
            )
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # 템플릿 렌더링
            template = Template(template_content)
            start_time, end_time = self.data_processor.get_yesterday_range()
            
            html_content = template.render(
                generation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                period=f"{start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}",
                total_sales=f"{summary_data.get('total_sales', 0):,}원",
                total_items=f"{summary_data.get('total_items', 0)}개",
                monthly_data=table2_data,
                table_data=table1_data
            )
            
            return html_content
            
        except Exception as e:
            self.logger.error(f"HTML 이메일 생성 실패: {str(e)}")
            return None
    
    def test_connection(self):
        """연결 테스트"""
        try:
            self.logger.info("연결 테스트 시작")
            
            # 이메일 연결 테스트
            if self.email_sender.test_connection():
                self.logger.info("이메일 연결 테스트 성공")
            else:
                self.logger.error("이메일 연결 테스트 실패")
            
            # 스프레드시트 연결 테스트
            try:
                self.spreadsheet_handler.get_main_sheet_data()
                self.logger.info("스프레드시트 연결 테스트 성공")
            except Exception as e:
                self.logger.error(f"스프레드시트 연결 테스트 실패: {str(e)}")
            
        except Exception as e:
            self.logger.error(f"연결 테스트 실패: {str(e)}")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='자판기 매출 관리 시스템')
    parser.add_argument('--schedule', action='store_true', help='스케줄러 모드로 실행')
    parser.add_argument('--test', action='store_true', help='연결 테스트 실행')
    parser.add_argument('--time', default='09:00', help='스케줄 실행 시간 (HH:MM)')
    
    args = parser.parse_args()
    
    # 로거 설정
    setup_logger()
    logger = get_logger()
    
    # 자동화 시스템 초기화
    automation = VendingMachineAutomation()
    
    if not automation.setup():
        logger.error("시스템 초기화 실패")
        sys.exit(1)
    
    if args.test:
        # 연결 테스트
        automation.test_connection()
        return
    
    if args.schedule:
        # 스케줄러 모드
        logger.info(f"스케줄러 모드 시작 - 실행 시간: {args.time}")
        
        # 매일 지정된 시간에 실행
        schedule.every().day.at(args.time).do(automation.run_automation)
        
        # 즉시 한 번 실행
        automation.run_automation()
        
        # 스케줄러 실행
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    else:
        # 즉시 실행
        logger.info("즉시 실행 모드")
        success = automation.run_automation()
        
        if success:
            logger.info("프로세스 완료")
        else:
            logger.error("프로세스 실패")
            sys.exit(1)

if __name__ == "__main__":
    main() 