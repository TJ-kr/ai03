import gspread
# from google.oauth2.service_account import Credentials  # 삭제
import pandas as pd
from datetime import datetime
from ..config.settings import Settings
from ..utils.logger import get_logger
from ..utils.helpers import is_duplicate_data, get_current_month
import os
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SpreadsheetHandler:
    def __init__(self):
        self.logger = get_logger()
        self.spreadsheet = None
        self.main_sheet = None
        self.table1_sheet = None
        self.table2_sheet = None
    
    def open_spreadsheet(self):
        """구글 스프레드시트 열기"""
        try:
            # API 인증 정보 설정
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            # 프로젝트 루트 기준으로 credentials 파일 경로 설정
            credentials_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'credentials',
                'google_credentials.json'
            )
            
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials 파일을 찾을 수 없습니다: {credentials_path}")
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credentials_path, scope)
            
            # gspread 클라이언트 생성
            gc = gspread.authorize(credentials)
            
            # 스프레드시트 열기 (ID 사용)
            self.spreadsheet = gc.open_by_key(Settings.SPREADSHEET_ID)
            self.main_sheet = self.spreadsheet.worksheet('main')
            self.table1_sheet = self.spreadsheet.worksheet('table1')
            self.table2_sheet = self.spreadsheet.worksheet('table2')
            
            self.logger.info("스프레드시트 연결 성공")
            return True
            
        except Exception as e:
            self.logger.error(f"스프레드시트 연결 실패: {str(e)}")
            return False
    
    def get_table1_data(self):
        """table1 시트의 A1:C20 데이터 추출"""
        try:
            if not self.table1_sheet:
                raise ValueError("table1 시트가 초기화되지 않았습니다.")
            
            # A1:C20 범위의 데이터 가져오기
            data = self.table1_sheet.get('A1:C20')
            return data
        
        except Exception as e:
            self.logger.error(f"table1 데이터 추출 실패: {str(e)}")
            return None
    
    def get_table2_monthly_data(self):
        """table2 시트에서 현재 월의 데이터 추출"""
        try:
            if not self.table2_sheet:
                raise ValueError("table2 시트가 초기화되지 않았습니다.")
            
            # 현재 월 구하기
            current_month = datetime.now().strftime('%Y-%m')
            
            # 모든 데이터 가져오기
            all_data = self.table2_sheet.get_all_values()
            if len(all_data) <= 1:  # 헤더만 있는 경우
                return None
            
            # A열에서 현재 월 데이터 찾기
            for row in all_data[1:]:  # 헤더 제외
                if row and current_month in str(row[0]):
                    return row
            
            return None
        
        except Exception as e:
            self.logger.error(f"table2 월별 데이터 추출 실패: {str(e)}")
            return None
    
    def get_main_sheet_data(self):
        """main 시트의 모든 데이터 가져오기"""
        try:
            worksheet = self.spreadsheet.worksheet(Settings.MAIN_SHEET)
            data = worksheet.get_all_values()
            self.logger.info(f"main 시트 데이터 로드 완료: {len(data)}행")
            return data
        except Exception as e:
            self.logger.error(f"main 시트 데이터 로드 실패: {str(e)}")
            raise
    
    def append_to_main_sheet(self, data):
        """main 시트에 데이터 추가 (중복 방지)"""
        try:
            worksheet = self.spreadsheet.worksheet(Settings.MAIN_SHEET)
            existing_data = worksheet.get_all_values()
            
            # 중복 확인
            if is_duplicate_data(data, existing_data):
                self.logger.warning("중복 데이터 발견. 추가하지 않습니다.")
                return False
            
            # 데이터 추가
            worksheet.append_row(data)
            self.logger.info("main 시트에 데이터 추가 완료")
            
            # H열 날짜+시간 서식 설정
            self._format_date_time_column(worksheet)
            
            return True
            
        except Exception as e:
            self.logger.error(f"main 시트 데이터 추가 실패: {str(e)}")
            raise
    
    def _format_date_time_column(self, worksheet):
        """H열 날짜+시간 서식 설정"""
        try:
            # 현재 데이터가 있는 행 수 확인
            all_values = worksheet.get_all_values()
            if len(all_values) <= 1:  # 헤더만 있는 경우
                return
            
            # H열의 마지막 행에 날짜+시간 서식 적용
            last_row = len(all_values)
            h_cell = f'H{last_row}'
            
            # H열이 날짜+시간 데이터인지 확인
            h_value = worksheet.acell(h_cell).value
            if h_value:
                try:
                    # gspread의 format 메서드 사용
                    worksheet.format(h_cell, {
                        "numberFormat": {
                            "type": "DATE_TIME",
                            "pattern": "yyyy-mm-dd hh:mm:ss"
                        }
                    })
                    self.logger.info(f"H열 서식 설정 완료: {h_cell}")
                except Exception as format_error:
                    self.logger.warning(f"gspread format 메서드 실패: {str(format_error)}")
                    
                    # 대안: Google Sheets API 직접 사용
                    try:
                        from googleapiclient.discovery import build
                        
                        # credentials 파일 경로
                        credentials_path = os.path.join(
                            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                            'credentials',
                            'google_credentials.json'
                        )
                        
                        # Google Sheets API 서비스 생성
                        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                            credentials_path, 
                            ['https://www.googleapis.com/auth/spreadsheets']
                        )
                        service = build('sheets', 'v4', credentials=credentials)
                        
                        # 스프레드시트 ID 추출 (URL에서)
                        spreadsheet_id = Settings.SPREADSHEET_ID
                        
                        # H열 전체에 날짜+시간 서식 적용
                        request = {
                            "requests": [
                                {
                                    "repeatCell": {
                                        "range": {
                                            "sheetId": 0,  # 첫 번째 시트 (main)
                                            "startRowIndex": 0,
                                            "endRowIndex": 1000,  # 충분히 큰 범위
                                            "startColumnIndex": 7,  # H열 (0부터 시작하므로 7)
                                            "endColumnIndex": 8
                                        },
                                        "cell": {
                                            "userEnteredFormat": {
                                                "numberFormat": {
                                                    "type": "DATE_TIME",
                                                    "pattern": "yyyy-mm-dd hh:mm:ss"
                                                }
                                            }
                                        },
                                        "fields": "userEnteredFormat(numberFormat)"
                                    }
                                }
                            ]
                        }
                        
                        # 서식 적용
                        service.spreadsheets().batchUpdate(
                            spreadsheetId=spreadsheet_id,
                            body=request
                        ).execute()
                        
                        self.logger.info(f"H열 전체 서식 설정 완료 (Google Sheets API 사용)")
                        
                    except Exception as api_error:
                        self.logger.error(f"Google Sheets API 서식 설정 실패: {str(api_error)}")
                        # 최종 대안: 수동으로 날짜+시간 형식 확인
                        self.logger.info(f"H열 날짜+시간 데이터 확인: {h_cell} = {h_value}")
            
        except Exception as e:
            self.logger.warning(f"H열 서식 설정 실패: {str(e)}")
            # 서식 설정 실패는 전체 프로세스를 중단하지 않음
    
    def create_dataframe_from_sheet(self, sheet_name, range_name=None):
        """시트 데이터를 DataFrame으로 변환"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            
            if range_name:
                data = worksheet.get(range_name)
            else:
                data = worksheet.get_all_values()
            
            if not data:
                return pd.DataFrame()
            
            # 첫 번째 행을 헤더로 사용
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
            
        except Exception as e:
            self.logger.error(f"시트 DataFrame 변환 실패: {str(e)}")
            raise
    
    def update_cell(self, sheet_name, cell, value):
        """특정 셀 업데이트"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            worksheet.update(cell, value)
            self.logger.info(f"{sheet_name} 시트 {cell} 셀 업데이트 완료")
        except Exception as e:
            self.logger.error(f"셀 업데이트 실패: {str(e)}")
            raise 