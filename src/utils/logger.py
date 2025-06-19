import os
import sys
from loguru import logger
from datetime import datetime

def setup_logger():
    """로거를 설정합니다."""
    # 기존 로거 제거
    logger.remove()
    
    # 콘솔 출력
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # 파일 출력
    log_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        'logs', 
        'automation.log'
    )
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    return logger

def get_logger():
    """로거 인스턴스를 반환합니다."""
    return logger

# 로거 초기화
setup_logger() 