#!/usr/bin/env python3
"""
다운로드된 Excel 파일 데이터 분석 스크립트
"""

import sys
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config.settings import Settings
from src.utils.helpers import get_latest_sales_file, extract_date_from_filename

def analyze_excel_file(file_path):
    """Excel 파일 분석"""
    print(f"📊 Excel 파일 분석: {os.path.basename(file_path)}")
    print("=" * 60)
    
    try:
        # Excel 파일 읽기
        df = pd.read_excel(file_path)
        
        print(f"📋 기본 정보:")
        print(f"   - 행 수: {len(df)}")
        print(f"   - 열 수: {len(df.columns)}")
        print(f"   - 파일 크기: {os.path.getsize(file_path):,} bytes")
        print()
        
        print("📋 컬럼 정보:")
        for i, col in enumerate(df.columns):
            print(f"   {i+1}. {col}")
        print()
        
        print("📋 처음 5행 데이터:")
        print(df.head().to_string(index=False))
        print()
        
        print("📋 마지막 5행 데이터:")
        print(df.tail().to_string(index=False))
        print()
        
        print("📋 처음 5행 데이터:")
        print(df.head().to_string(index=False))
        print()
        
        print("📋 마지막 5행 데이터:")
        print(df.tail().to_string(index=False))
        print()
        
        print("📋 데이터 타입:")
        print(df.dtypes)
        print()
        
        print("📋 기본 통계:")
        print(df.describe())
        print()
        
        # 날짜 컬럼 찾기
        date_columns = []
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['날짜', 'date', '시간', 'time']):
                date_columns.append(col)
        
        if date_columns:
            print(f"📅 날짜 관련 컬럼: {date_columns}")
            for col in date_columns:
                print(f"   - {col}: {df[col].min()} ~ {df[col].max()}")
        else:
            print("⚠️  날짜 관련 컬럼을 찾을 수 없습니다")
        
        print()
        
        # 매출 관련 컬럼 찾기
        sales_columns = []
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['매출', '금액', '가격', 'sales', 'amount', 'price']):
                sales_columns.append(col)
        
        if sales_columns:
            print(f"💰 매출 관련 컬럼: {sales_columns}")
            for col in sales_columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    print(f"   - {col}: 총 {df[col].sum():,}원")
        else:
            print("⚠️  매출 관련 컬럼을 찾을 수 없습니다")
        
        return df
        
    except Exception as e:
        print(f"❌ 파일 분석 실패: {str(e)}")
        return None

def prepare_spreadsheet_data(df):
    """스프레드시트용 데이터 준비"""
    print("📝 스프레드시트용 데이터 준비")
    print("=" * 40)
    
    # 헤더 (컬럼명)
    headers = df.columns.tolist()
    print(f"📋 헤더: {headers}")
    
    # 데이터 행들
    data_rows = df.values.tolist()
    print(f"📊 데이터 행 수: {len(data_rows)}")
    
    # 스프레드시트용 데이터 (헤더 + 데이터)
    spreadsheet_data = [headers] + data_rows
    
    print("✅ 스프레드시트용 데이터 준비 완료")
    return spreadsheet_data

def main():
    """메인 함수"""
    print("🔍 Excel 파일 데이터 분석")
    print("=" * 70)
    
    # 다운로드 폴더에서 최신 파일 찾기
    download_dir = Settings.DOWNLOAD_DIR
    latest_file = get_latest_sales_file(download_dir)
    
    if not latest_file or not os.path.exists(latest_file):
        print("❌ 다운로드된 Excel 파일을 찾을 수 없습니다")
        return
    
    # 파일명에서 날짜 추출
    filename = os.path.basename(latest_file)
    file_date = extract_date_from_filename(filename)
    
    print(f"📁 분석할 파일: {filename}")
    if file_date:
        print(f"📅 파일 날짜: {file_date}")
    print()
    
    # Excel 파일 분석
    df = analyze_excel_file(latest_file)
    
    if df is not None:
        # 스프레드시트용 데이터 준비
        spreadsheet_data = prepare_spreadsheet_data(df)
        
        print("\n🎯 다음 단계:")
        print("1. 이 데이터를 구글 스프레드시트 'main' 시트에 추가")
        print("2. 중복 데이터 방지 로직 구현")
        print("3. 날짜별 데이터 구분 및 처리")

if __name__ == "__main__":
    main() 