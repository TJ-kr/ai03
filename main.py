#!/usr/bin/env python3
"""
자판기 매출 자동화 시스템 - 메인 실행 파일
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 프로젝트 루트 경로 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 환경 변수 로드
load_dotenv()

from src.web_automation.download import download_sales_excel
from src.google_drive.upload import upload_sales_excel
from src.data_processing.excel_parser import parse_sales_excel, calculate_daily_sales
from src.data_processing.sales_calculator import calculate_inventory_changes, calculate_monthly_sales, generate_sales_report
from src.email_system.sender import send_sales_report_email
from src.utils.logger import get_logger
from src.utils.error_handler import safe_action, retry_on_error

logger = get_logger()

@safe_action("자판기 매출 자동화")
def run_automation():
    """전체 자동화 프로세스를 실행합니다."""
    
    logger.info("=== 자판기 매출 자동화 시작 ===")
    
    # 1단계: 웹사이트에서 엑셀 다운로드
    logger.info("1단계: 매출 데이터 다운로드 시작")
    excel_file_path = download_sales_excel()
    
    if not excel_file_path:
        logger.error("엑셀 파일 다운로드 실패")
        return False
    
    logger.info(f"엑셀 파일 다운로드 완료: {excel_file_path}")
    
    # 2단계: 구글 드라이브 업로드
    logger.info("2단계: 구글 드라이브 업로드 시작")
    upload_result = upload_sales_excel(excel_file_path)
    
    if upload_result:
        logger.info("구글 드라이브 업로드 완료")
    else:
        logger.warning("구글 드라이브 업로드 실패 (계속 진행)")
    
    # 3단계: 데이터 처리
    logger.info("3단계: 데이터 처리 시작")
    sheets_data = parse_sales_excel(excel_file_path)
    
    if not sheets_data:
        logger.error("엑셀 파일 파싱 실패")
        return False
    
    # 매출 데이터 계산
    daily_sales = calculate_daily_sales(sheets_data)
    inventory_changes = calculate_inventory_changes(sheets_data)
    monthly_sales = calculate_monthly_sales(sheets_data)
    
    # 보고서 생성
    report_data = generate_sales_report(daily_sales, inventory_changes, monthly_sales)
    
    logger.info("데이터 처리 완료")
    
    # 4단계: 이메일 발송
    logger.info("4단계: 이메일 발송 시작")
    email_result = send_sales_report_email(report_data, excel_file_path)
    
    if email_result:
        logger.info("이메일 발송 완료")
    else:
        logger.error("이메일 발송 실패")
    
    logger.info("=== 자판기 매출 자동화 완료 ===")
    return True

def main():
    """메인 함수"""
    try:
        success = run_automation()
        if success:
            print("✅ 자동화 프로세스가 성공적으로 완료되었습니다.")
            sys.exit(0)
        else:
            print("❌ 자동화 프로세스 중 오류가 발생했습니다.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"예상치 못한 오류: {e}")
        print(f"❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 