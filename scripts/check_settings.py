#!/usr/bin/env python3
"""
설정 확인 스크립트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config.settings import Settings

def main():
    print("📋 현재 설정 확인")
    print("=" * 50)
    
    print(f"EMAIL_SENDER: {Settings.EMAIL_SENDER}")
    print(f"EMAIL_PASSWORD: {'*' * len(Settings.EMAIL_PASSWORD) if Settings.EMAIL_PASSWORD else '설정되지 않음'}")
    print(f"EMAIL_RECIPIENTS: {Settings.EMAIL_RECIPIENTS}")
    
    print(f"\nWEBSITE_URL: {Settings.WEBSITE_URL}")
    print(f"WEBSITE_USERNAME: {Settings.WEBSITE_USERNAME}")
    print(f"WEBSITE_PASSWORD: {'*' * len(Settings.WEBSITE_PASSWORD) if Settings.WEBSITE_PASSWORD else '설정되지 않음'}")
    
    print(f"\nSPREADSHEET_ID: {Settings.SPREADSHEET_ID}")
    print(f"GOOGLE_CREDENTIALS_FILE: {Settings.GOOGLE_CREDENTIALS_FILE}")

if __name__ == "__main__":
    main() 