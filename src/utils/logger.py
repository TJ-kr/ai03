import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name='vending_machine'):
    """로거 설정"""
    # 로그 디렉토리 생성
    log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # 로그 파일명 설정 (날짜별)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f'{today}.log'
    
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 이미 핸들러가 있다면 제거
    if logger.handlers:
        logger.handlers.clear()
    
    # 파일 핸들러 추가
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포맷터 설정
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name='vending_machine'):
    """기존 로거 가져오기"""
    return logging.getLogger(name) 