# 🐙 GitHub Actions 설정 가이드

GitHub Actions를 사용하여 무료로 24/7 자동 데이터 수집을 설정하는 방법입니다.

## 📋 1단계: GitHub 저장소 생성

### 1.1 GitHub 계정 생성 (이미 있다면 생략)
1. [GitHub.com](https://github.com) 접속
2. "Sign up" 클릭하여 계정 생성

### 1.2 새 저장소 생성
1. GitHub 로그인 후 우측 상단 "+" → "New repository" 클릭
2. 저장소 설정:
   - **Repository name**: `toygo-vending-automation`
   - **Description**: `TOYGO 자판기 매출 데이터 자동 수집 시스템`
   - **Visibility**: Private (보안상 권장)
   - **Initialize**: 체크하지 않음
3. "Create repository" 클릭

## 📋 2단계: 로컬 코드를 GitHub에 업로드

### 2.1 Git 초기화 및 업로드
```bash
# 프로젝트 디렉토리로 이동
cd vending_machine_automation

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 번째 커밋
git commit -m "Initial commit: TOYGO 자판기 매출 데이터 수집 시스템"

# GitHub 저장소 연결 (YOUR_USERNAME을 실제 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/toygo-vending-automation.git

# 코드 업로드
git branch -M main
git push -u origin main
```

### 2.2 .gitignore 파일 확인
중요한 파일들이 업로드되지 않도록 `.gitignore` 파일을 확인하세요:

```
# 환경 변수 파일
.env

# Google Credentials
credentials/google_credentials.json

# 다운로드된 파일
downloads/

# 로그 파일
logs/

# Python 캐시
__pycache__/
*.pyc

# 가상환경
venv/
env/
```

## 📋 3단계: GitHub Secrets 설정

### 3.1 Google Cloud 서비스 계정 키 생성
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 선택
3. "IAM 및 관리" → "서비스 계정" 클릭
4. "서비스 계정 만들기" 클릭
5. 설정:
   - **서비스 계정 이름**: `github-actions`
   - **설명**: `GitHub Actions용 서비스 계정`
6. "만들고 계속하기" 클릭
7. 권한 설정:
   - **역할**: `편집자` 선택
8. "완료" 클릭

### 3.2 서비스 계정 키 다운로드
1. 생성된 서비스 계정 클릭
2. "키" 탭 클릭
3. "키 추가" → "새 키 만들기" 클릭
4. **JSON** 형식 선택
5. 키 파일 다운로드

### 3.3 GitHub Secrets 등록
1. GitHub 저장소 페이지에서 "Settings" 탭 클릭
2. 좌측 메뉴에서 "Secrets and variables" → "Actions" 클릭
3. "New repository secret" 클릭하여 다음 2개 추가:

#### GOOGLE_CREDENTIALS
- **Name**: `GOOGLE_CREDENTIALS`
- **Value**: 다운로드한 JSON 파일의 전체 내용을 복사하여 붙여넣기

#### GOOGLE_PROJECT_ID
- **Name**: `GOOGLE_PROJECT_ID`
- **Value**: Google Cloud 프로젝트 ID (예: `my-project-123456`)

## 📋 4단계: GitHub Actions 활성화

### 4.1 Actions 탭 확인
1. GitHub 저장소에서 "Actions" 탭 클릭
2. "TOYGO Data Collector" 워크플로우가 보이는지 확인
3. "Run workflow" 버튼으로 수동 테스트 가능

### 4.2 자동 실행 확인
- 매일 오전 9시 (한국 시간)에 자동 실행
- UTC 00:00 = 한국 시간 09:00

## 📋 5단계: 모니터링 및 관리

### 5.1 실행 상태 확인
1. "Actions" 탭에서 실행 기록 확인
2. 각 실행의 상세 로그 확인 가능
3. 실패 시 오류 메시지 확인

### 5.2 로그 다운로드
1. 실행 완료 후 "Artifacts" 섹션에서 로그 다운로드
2. 로그는 7일간 보관됨

### 5.3 수동 실행
1. "Actions" 탭에서 "Run workflow" 클릭
2. 언제든지 수동으로 데이터 수집 실행 가능

## 🔧 문제 해결

### 일반적인 문제
1. **Secrets 설정 오류**: JSON 형식 확인
2. **권한 오류**: 서비스 계정 권한 확인
3. **의존성 오류**: requirements.txt 확인

### 디버깅
```bash
# 로컬에서 테스트
python scripts/data_collector.py

# GitHub Actions 로그 확인
# Actions 탭에서 각 실행의 상세 로그 확인
```

## 📊 예상 결과

### 성공 시
- ✅ 매일 오전 9시 자동 실행
- ✅ 스프레드시트에 데이터 자동 추가
- ✅ 실행 로그 자동 저장
- ✅ 완전 무료 운영

### 모니터링
- GitHub Actions에서 실행 상태 실시간 확인
- 이메일 알림 설정 가능
- 로그 파일 자동 보관

## 📞 지원

문제가 발생하면:
1. GitHub Actions 로그 확인
2. Secrets 설정 재확인
3. Google Cloud 권한 확인
4. 로컬 테스트로 문제 격리 