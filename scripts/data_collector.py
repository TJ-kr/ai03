#!/usr/bin/env python3
"""
데이터 수집기 - 로그인부터 스프레드시트 데이터 입력까지
이메일 발송 없이 데이터 수집만 수행
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.services.web_scraper import WebScraper
from src.services.spreadsheet_handler import SpreadsheetHandler
from src.services.data_processor import DataProcessor
from src.config.settings import Settings
from src.utils.logger import setup_logger, get_logger

class DataCollector:
    def __init__(self):
        self.logger = get_logger()
        self.spreadsheet_handler = None
        self.data_processor = None
    
    def setup(self):
        """시스템 초기 설정"""
        try:
            # 설정 검증
            Settings.validate_settings()
            
            # 필요한 디렉토리 생성
            from src.utils.helpers import ensure_directory
            ensure_directory(Settings.DOWNLOAD_DIR)
            ensure_directory(Settings.LOGS_DIR)
            
            # 서비스 초기화
            self.spreadsheet_handler = SpreadsheetHandler()
            self.data_processor = DataProcessor()
            
            # 스프레드시트 열기
            self.spreadsheet_handler.open_spreadsheet()
            
            self.logger.info("데이터 수집기 초기화 완료")
            return True
            
        except Exception as e:
            self.logger.error(f"데이터 수집기 초기화 실패: {str(e)}")
            return False
    
    def collect_data(self):
        """데이터 수집 프로세스 실행"""
        try:
            self.logger.info("데이터 수집 프로세스 시작")
            
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
            
            self.logger.info("데이터 수집 프로세스 완료")
            return True
            
        except Exception as e:
            self.logger.error(f"데이터 수집 프로세스 실패: {str(e)}")
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

def main():
    """메인 함수"""
    # 로거 설정
    setup_logger()
    
    print("📊 TOYGO 자판기 매출 데이터 수집기")
    print("=" * 60)
    print("📋 실행 프로세스:")
    print("   1. 웹사이트 로그인 및 매출 데이터 다운로드")
    print("   2. 다운로드된 파일 처리 및 데이터 추출")
    print("   3. 구글 스프레드시트에 데이터 추가")
    print("=" * 60)
    
    # 데이터 수집기 초기화
    collector = DataCollector()
    
    if not collector.setup():
        print("❌ 시스템 초기화 실패")
        return
    
    # 데이터 수집 실행
    print("\n🚀 데이터 수집 시작...")
    success = collector.collect_data()
    
    if success:
        print("\n✅ 데이터 수집 완료!")
        print("스프레드시트에 데이터가 정상적으로 추가되었습니다.")
    else:
        print("\n❌ 데이터 수집 실패")
        print("로그 파일을 확인하여 오류를 확인해주세요.")

if __name__ == "__main__":
    main() 