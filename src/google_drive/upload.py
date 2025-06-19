import os
from datetime import datetime
from .auth import get_google_drive_service
from ..utils.logger import get_logger

def upload_to_google_drive(file_path, folder_id=None):
    """파일을 구글 드라이브에 업로드합니다."""
    try:
        service = get_google_drive_service()
        
        # 파일명 생성 (날짜_시간_원본파일명)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{name}{ext}"
        
        # 파일 메타데이터 설정
        file_metadata = {
            'name': new_filename,
            'parents': [folder_id] if folder_id else []
        }
        
        # 파일 업로드
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        print(f"파일 업로드 성공: {new_filename}")
        print(f"구글 드라이브 링크: {file.get('webViewLink')}")
        
        return file.get('id')
        
    except Exception as e:
        print(f"구글 드라이브 업로드 실패: {e}")
        return None

def upload_sales_excel(excel_file_path):
    """매출 엑셀 파일을 구글 드라이브에 업로드합니다."""
    # config에서 폴더 ID 가져오기 (환경변수에서)
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    if not folder_id:
        print("GOOGLE_DRIVE_FOLDER_ID 환경변수가 설정되지 않았습니다.")
        return None
    
    return upload_to_google_drive(excel_file_path, folder_id) 