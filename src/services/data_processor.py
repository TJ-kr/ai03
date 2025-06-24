import pandas as pd
from datetime import datetime
from ..utils.logger import get_logger
from ..utils.helpers import parse_excel_file, create_summary_data, format_currency, get_yesterday_range

class DataProcessor:
    def __init__(self):
        self.logger = get_logger()
    
    def process_downloaded_file(self, file_path):
        """다운로드된 파일 처리"""
        try:
            self.logger.info(f"파일 처리 시작: {file_path}")
            
            # 파일 읽기
            df = parse_excel_file(file_path)
            
            if df.empty:
                raise Exception("파일이 비어있습니다")
            
            # 데이터 정리
            df = self._clean_data(df)
            
            # 요약 데이터 생성
            summary = create_summary_data(df)
            
            # 스프레드시트용 데이터 준비
            spreadsheet_data = self._prepare_spreadsheet_data(df)
            
            self.logger.info("파일 처리 완료")
            return {
                'dataframe': df,
                'summary': summary,
                'spreadsheet_data': spreadsheet_data
            }
            
        except Exception as e:
            self.logger.error(f"파일 처리 실패: {str(e)}")
            raise
    
    def _clean_data(self, df):
        """데이터 정리"""
        # 빈 행 제거
        df = df.dropna(how='all')
        
        # 빈 열 제거
        df = df.dropna(axis=1, how='all')
        
        # 컬럼명 정리
        df.columns = df.columns.str.strip()
        
        return df
    
    def _prepare_spreadsheet_data(self, df):
        """스프레드시트용 데이터 준비"""
        # 첫 번째 행을 헤더로 사용하고 나머지를 데이터로 변환
        data = [df.columns.tolist()] + df.values.tolist()
        return data
    
    def create_email_content(self, summary_data, table1_data, table2_monthly_data):
        """이메일 내용 생성"""
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 기본 내용 구성
            content = [
                "📊 자판기 매출 보고서",
                f"생성일시: {now}\n",
            ]
            
            # 일일 매출 요약
            if summary_data:
                # 실제 키 이름에 맞게 수정
                period = summary_data.get('period', '기간 정보 없음')
                total_sales = summary_data.get('total_sales', 0)
                total_items = summary_data.get('total_items', 0)
                
                content.extend([
                    "📈 일일 매출 요약",
                    f"기간: {period}",
                    f"매출액: {total_sales:,}원",
                    f"판매 상품 수: {total_items}개\n"
                ])
            
            # 재고 현황 (임시)
            content.extend([
                "📦 재고 현황",
                "재고 상태: 정상\n"
            ])
            
            # 월 누적 매출
            if table2_monthly_data:
                content.extend([
                    "📅 월 누적 매출",
                    f"{table2_monthly_data[0]}: {table2_monthly_data[1]}\n"
                ])
            
            # 총계 (table1 데이터)
            if table1_data:
                content.append("💰 총계")
                content.append("=" * 50)  # 구분선 추가
                
                # 헤더 행
                if len(table1_data) > 0:
                    header_row = table1_data[0]
                    header_line = " | ".join(str(cell).center(15) for cell in header_row)
                    content.append(header_line)
                    content.append("-" * len(header_line))  # 헤더 구분선
                
                # 데이터 행들
                for row in table1_data[1:]:
                    if row:  # 빈 행이 아닌 경우만
                        data_line = " | ".join(str(cell).center(15) for cell in row)
                        content.append(data_line)
                
                content.append("=" * 50)  # 끝 구분선
                content.append("")  # 빈 줄 추가
            
            return "\n".join(content)
            
        except Exception as e:
            self.logger.error(f"이메일 내용 생성 실패: {str(e)}")
            return None
    
    def _format_table_data(self, table_data):
        """테이블 데이터를 포맷팅"""
        if not table_data:
            return "데이터 없음\n"
        
        formatted = ""
        for row in table_data:
            if row:
                formatted += " | ".join(str(cell) for cell in row) + "\n"
        
        return formatted
    
    def extract_summary_from_dataframe(self, df):
        """DataFrame에서 요약 정보 추출"""
        try:
            summary = {
                'total_sales': 0,
                'total_items': len(df),
                'period': "기간 정보 없음"
            }
            
            # 매출 컬럼 찾기
            sales_columns = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['매출', '금액', '가격', 'sales', 'amount', 'price'])]
            
            if sales_columns:
                # 숫자형으로 변환 시도
                try:
                    df[sales_columns[0]] = pd.to_numeric(df[sales_columns[0]], errors='coerce')
                    summary['total_sales'] = df[sales_columns[0]].sum()
                except:
                    pass
            
            # 날짜 컬럼 찾기
            date_columns = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['날짜', 'date', '시간', 'time'])]
            
            if date_columns:
                try:
                    df[date_columns[0]] = pd.to_datetime(df[date_columns[0]], errors='coerce')
                    min_date = df[date_columns[0]].min()
                    max_date = df[date_columns[0]].max()
                    if pd.notna(min_date) and pd.notna(max_date):
                        summary['period'] = f"{min_date.strftime('%Y-%m-%d')} ~ {max_date.strftime('%Y-%m-%d')}"
                except:
                    pass
            
            return summary
            
        except Exception as e:
            self.logger.error(f"요약 정보 추출 실패: {str(e)}")
            return {
                'total_sales': 0,
                'total_items': 0,
                'period': "오류 발생"
            } 