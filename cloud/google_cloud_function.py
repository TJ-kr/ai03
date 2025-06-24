#!/usr/bin/env python3
"""
Google Cloud Functions - TOYGO 자판기 매출 데이터 수집
서버리스 환경에서 실행되는 함수
"""

import os
import json
import tempfile
from datetime import datetime
import logging

# Google Cloud Functions 환경 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/tmp/google_credentials.json'

# 프로젝트 모듈 import
import sys
sys.path.append('/tmp')

from src.services.web_scraper import WebScraper
from src.services.spreadsheet_handler import SpreadsheetHandler
from src.services.data_processor import DataProcessor
from src.config.settings import Settings
from src.utils.logger import setup_logger, get_logger

def setup_environment():
    """클라우드 환경 설정"""
    # 임시 디렉토리 생성
    os.makedirs('/tmp/downloads', exist_ok=True)
    os.makedirs('/tmp/logs', exist_ok=True)
    
    # 환경 변수 설정
    os.environ['DOWNLOAD_DIR'] = '/tmp/downloads'
    os.environ['LOGS_DIR'] = '/tmp/logs'
    
    # Google Credentials 설정
    credentials_content = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    if credentials_content:
        with open('/tmp/google_credentials.json', 'w') as f:
            f.write(credentials_content)

def collect_data_cloud(request):
    """Cloud Functions 메인 함수"""
    try:
        # 환경 설정
        setup_environment()
        setup_logger()
        logger = get_logger()
        
        logger.info("클라우드 데이터 수집 시작")
        
        # 1. 웹사이트에서 파일 다운로드
        downloaded_file = None
        with WebScraper() as scraper:
            scraper.login()
            downloaded_file = scraper.download_file()
        
        if not downloaded_file:
            logger.error("파일 다운로드 실패")
            return json.dumps({"success": False, "error": "파일 다운로드 실패"})
        
        # 2. 파일 처리
        data_processor = DataProcessor()
        processed_data = data_processor.process_downloaded_file(downloaded_file)
        
        if not processed_data:
            logger.error("파일 처리 실패")
            return json.dumps({"success": False, "error": "파일 처리 실패"})
        
        # 3. 스프레드시트 업데이트
        spreadsheet_handler = SpreadsheetHandler()
        spreadsheet_handler.open_spreadsheet()
        
        success_count = 0
        for row in processed_data['spreadsheet_data'][1:]:  # 헤더 제외
            if spreadsheet_handler.append_to_main_sheet(row):
                success_count += 1
        
        logger.info(f"데이터 수집 완료: {success_count}개 행 추가")
        
        # 임시 파일 정리
        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        
        return json.dumps({
            "success": True,
            "message": f"데이터 수집 완료: {success_count}개 행 추가",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"클라우드 데이터 수집 실패: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })

# HTTP 트리거용 함수
def http_collect_data(request):
    """HTTP 요청으로 트리거되는 함수"""
    return collect_data_cloud(request)

# Pub/Sub 트리거용 함수
def pubsub_collect_data(event, context):
    """Pub/Sub 메시지로 트리거되는 함수"""
    return collect_data_cloud(None) 