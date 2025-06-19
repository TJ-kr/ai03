import os
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# 환경 변수 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# 구글 드라이브 API 스코프
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_google_drive_service():
    """구글 드라이브 API 서비스 객체를 반환합니다."""
    creds = None
    
    # 서비스 계정 키 파일 경로
    service_account_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        'credentials', 
        'google_credentials.json'
    )
    
    # 서비스 계정 키 파일이 있으면 사용
    if os.path.exists(service_account_file):
        creds = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
    else:
        # OAuth 2.0 클라이언트 ID 파일 사용 (개발용)
        client_secrets_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'credentials', 
            'client_secrets.json'
        )
        
        if os.path.exists(client_secrets_file):
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            raise FileNotFoundError("구글 인증 파일이 없습니다. credentials 폴더에 google_credentials.json 또는 client_secrets.json을 추가하세요.")
    
    # 토큰이 만료되었으면 갱신
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    return build('drive', 'v3', credentials=creds) 