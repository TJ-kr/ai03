# 구글 드라이브 인증 파일 설정

## 📁 필요한 파일

이 폴더에 다음 파일 중 하나를 추가해야 합니다:

### 1. 서비스 계정 키 (권장)
- **파일명**: `google_credentials.json`
- **용도**: 서버/자동화 환경에서 사용
- **설정 방법**: 아래 안내 참조

### 2. OAuth 클라이언트 ID (개발용)
- **파일명**: `client_secrets.json`
- **용도**: 개발/테스트 환경에서 사용
- **설정 방법**: 아래 안내 참조

## 🔧 서비스 계정 설정 (권장)

### 1. Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 또는 선택

### 2. Google Drive API 활성화
1. "API 및 서비스" → "라이브러리" 클릭
2. "Google Drive API" 검색 후 활성화

### 3. 서비스 계정 생성
1. "API 및 서비스" → "사용자 인증 정보" 클릭
2. "사용자 인증 정보 만들기" → "서비스 계정" 선택
3. 서비스 계정 이름 입력 (예: "vending-automation")
4. "키 만들기" → "JSON" 선택
5. 다운로드된 JSON 파일을 `google_credentials.json`으로 저장

### 4. 구글 드라이브 폴더 공유
1. 업로드할 구글 드라이브 폴더 열기
2. 폴더 우클릭 → "공유" 클릭
3. 서비스 계정 이메일 추가 (JSON 파일의 `client_email` 값)
4. 권한: "편집자" 설정

### 5. 환경 변수 설정
`.env` 파일에 다음 추가:
```env
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
```

## 🔧 OAuth 클라이언트 설정 (개발용)

### 1. OAuth 클라이언트 ID 생성
1. Google Cloud Console → "사용자 인증 정보"
2. "사용자 인증 정보 만들기" → "OAuth 클라이언트 ID"
3. 애플리케이션 유형: "데스크톱 앱" 선택
4. 다운로드된 JSON 파일을 `client_secrets.json`으로 저장

### 2. 첫 실행 시 인증
- 프로그램 실행 시 브라우저가 열리며 구글 계정 인증 필요
- 인증 후 토큰이 자동으로 저장됨

## 📋 폴더 ID 확인 방법

1. 구글 드라이브에서 업로드할 폴더 열기
2. URL에서 폴더 ID 확인:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
   ```
3. `FOLDER_ID_HERE` 부분이 폴더 ID

## ⚠️ 주의사항

- 인증 파일은 절대 Git에 커밋하지 마세요
- `.gitignore`에 `credentials/` 폴더가 포함되어 있는지 확인
- 서비스 계정 키는 안전하게 보관하세요

## 🧪 테스트

인증 파일 설정 후 다음 명령으로 테스트:
```bash
python -c "from src.google_drive.auth import get_google_drive_service; print('인증 성공!')" 