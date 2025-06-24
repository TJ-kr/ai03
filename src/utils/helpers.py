import os
import glob
from datetime import datetime, timedelta
import pandas as pd
import re

def ensure_directory(directory):
    """디렉토리가 존재하지 않으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_latest_file(directory, pattern="*"):
    """지정된 디렉토리에서 가장 최근 파일 찾기"""
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def format_currency(amount):
    """금액을 한국어 형식으로 포맷팅"""
    if amount is None:
        return "0원"
    return f"{int(amount):,}원"

def format_datetime(dt):
    """날짜시간을 한국어 형식으로 포맷팅"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_yesterday_range():
    """어제 날짜의 시작과 끝 시간 반환"""
    yesterday = datetime.now() - timedelta(days=1)
    start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_time, end_time

def get_current_month():
    """현재 월 반환 (YYYY-MM 형식)"""
    return datetime.now().strftime("%Y-%m")

def is_duplicate_data(data, existing_data):
    """중복 데이터인지 확인"""
    if not existing_data or len(existing_data) == 0:
        return False
    
    # 첫 번째 행이 헤더인 경우 제외
    if len(existing_data) > 1:
        existing_data = existing_data[1:]
    
    # 날짜 기준으로 중복 확인 (첫 번째 컬럼이 날짜라고 가정)
    data_date = data[0] if data else None
    
    for row in existing_data:
        if row and len(row) > 0 and row[0] == data_date:
            return True
    
    return False

def parse_excel_file(file_path):
    """Excel 파일을 pandas DataFrame으로 읽기"""
    try:
        # 파일 확장자 확인
        if file_path.endswith('.xlsx'):
            return pd.read_excel(file_path, engine='openpyxl')
        elif file_path.endswith('.xls'):
            return pd.read_excel(file_path, engine='xlrd')
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path, encoding='utf-8')
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {file_path}")
    except Exception as e:
        raise Exception(f"파일 읽기 실패: {str(e)}")

def create_summary_data(df, date_column=None):
    """DataFrame에서 요약 데이터 생성"""
    if df.empty:
        return {
            'total_sales': 0,
            'total_items': 0,
            'period': "데이터 없음"
        }
    
    # 매출 컬럼 찾기 (금액 관련 컬럼)
    sales_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['매출', '금액', '가격', 'sales', 'amount', 'price'])]
    
    if sales_columns:
        total_sales = df[sales_columns[0]].sum()
    else:
        total_sales = 0
    
    total_items = len(df)
    
    # 기간 정보
    if date_column and date_column in df.columns:
        start_date = df[date_column].min()
        end_date = df[date_column].max()
        period = f"{start_date} ~ {end_date}"
    else:
        period = "기간 정보 없음"
    
    return {
        'total_sales': total_sales,
        'total_items': total_items,
        'period': period
    }

def get_latest_sales_file(directory, date=None):
    """특정 날짜의 매출 파일 또는 최신 파일 찾기"""
    if date is None:
        # 날짜가 지정되지 않으면 어제 날짜 사용
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Sell_Total{날짜}.xlsx 패턴으로 파일 찾기
    pattern = f"Sell_Total{date}.xlsx"
    file_path = os.path.join(directory, pattern)
    
    if os.path.exists(file_path):
        return file_path
    
    # 해당 날짜 파일이 없으면 최신 파일 반환
    return get_latest_file(directory, "Sell_Total*.xlsx")

def extract_date_from_filename(filename):
    """파일명에서 날짜 추출"""
    # Sell_Total2025-06-19.xlsx 패턴에서 날짜 추출
    match = re.search(r'Sell_Total(\d{4}-\d{2}-\d{2})\.xlsx', filename)
    if match:
        return match.group(1)
    return None 