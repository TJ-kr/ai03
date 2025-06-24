import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 로드
load_dotenv()

class Settings:
    # 웹사이트 설정
    WEBSITE_URL = os.getenv('WEBSITE_URL', '')
    WEBSITE_USERNAME = os.getenv('WEBSITE_USERNAME', '')
    WEBSITE_PASSWORD = os.getenv('WEBSITE_PASSWORD', '')
    
    # 구글 스프레드시트 설정
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1PckoSzEWtsxt6seKG-n8wms_00G-cTf7eNjR6Rj-ggE')
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials/google_credentials.json')
    
    # 이메일 설정
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    
    # 로그 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/vending_machine.log')
    
    # 파일 경로 설정
    DOWNLOAD_DIR = 'downloads'
    LOGS_DIR = 'logs'
    
    # 스프레드시트 시트 이름
    MAIN_SHEET = 'main'
    TABLE1_SHEET = 'table1'
    TABLE2_SHEET = 'table2'
    
    # 이메일 템플릿 설정
    EMAIL_SUBJECT = '📊 자판기 매출 보고서'
    
    @classmethod
    def validate_settings(cls):
        """필수 설정값 검증"""
        required_settings = [
            ('WEBSITE_URL', cls.WEBSITE_URL),
            ('WEBSITE_USERNAME', cls.WEBSITE_USERNAME),
            ('WEBSITE_PASSWORD', cls.WEBSITE_PASSWORD),
            ('EMAIL_SENDER', cls.EMAIL_SENDER),
            ('EMAIL_PASSWORD', cls.EMAIL_PASSWORD),
        ]
        
        missing_settings = []
        for name, value in required_settings:
            if not value:
                missing_settings.append(name)
        
        if missing_settings:
            raise ValueError(f"필수 설정이 누락되었습니다: {', '.join(missing_settings)}")
        
        return True 