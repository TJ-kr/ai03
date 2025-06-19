# 자판기 매출 자동화 시스템

## 📋 프로젝트 개요
자판기 관제시스템에서 매출 데이터를 자동으로 수집, 처리, 보고하는 시스템입니다.

## 🎯 주요 기능
1. **자동 로그인**: 매일 오전 9:50에 자판기 관제시스템 자동 로그인
2. **데이터 다운로드**: 매출 자료를 엑셀 파일로 자동 다운로드
3. **구글 드라이브 업로드**: 다운로드된 파일을 구글 드라이브에 자동 업로드
4. **데이터 처리**: 매출, 재고량, 월 누적 매출 계산
5. **이메일 보고**: 처리된 정보를 이메일로 자동 발송

## 🏗️ 프로젝트 구조
```
vending_machine_automation/
├── src/                    # 소스 코드
│   ├── web_automation/     # 웹 자동화
│   ├── google_drive/       # 구글 드라이브 연동
│   ├── data_processing/    # 데이터 처리
│   ├── email_system/       # 이메일 시스템
│   └── utils/              # 유틸리티
├── data/                   # 데이터 저장소
├── logs/                   # 로그 파일
├── credentials/            # 인증 파일
└── tests/                  # 테스트 파일
```

## 🚀 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 정보를 입력하세요:
```env
# 자판기 관제시스템 로그인 정보
VENDING_LOGIN_ID=locolor
VENDING_LOGIN_PASSWORD=locolor2025

# 구글 드라이브 설정
GOOGLE_DRIVE_FOLDER_ID=your_folder_id

# 이메일 설정
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAILS=recipient1@email.com,recipient2@email.com
```

### 3. 구글 드라이브 인증 설정
1. Google Cloud Console에서 프로젝트 생성
2. Google Drive API 활성화
3. 서비스 계정 생성 및 키 다운로드
4. `credentials/google_credentials.json`에 저장

## 📅 마일스톤

### ✅ 마일스톤 1: 프로젝트 기반 구조 구축 (완료)
- [x] 프로젝트 디렉토리 구조 생성
- [x] Git 저장소 초기화 및 .gitignore 설정
- [x] 환경 변수 관리 시스템 구축
- [x] 의존성 관리 파일 생성
- [x] 기본 설정 파일 생성

### 🔄 진행 중인 마일스톤
- [ ] 마일스톤 2: 웹 자동화 시스템 구축
- [ ] 마일스톤 3: 구글 드라이브 연동
- [ ] 마일스톤 4: 데이터 처리 엔진
- [ ] 마일스톤 5: 이메일 보고 시스템
- [ ] 마일스톤 6: 스케줄링 및 배포
- [ ] 마일스톤 7: 통합 및 최적화

## 🔧 사용법

### 수동 실행
```bash
python main.py
```

### 자동 스케줄링
Windows Task Scheduler를 사용하여 매일 오전 9:50에 자동 실행

## 📊 데이터 처리 규칙
- **매출 기간**: 전날 오전 9:50 ~ 당일 오전 9:50
- **재고량 계산**: 입력 재고 - 판매 재고
- **월 누적 매출**: 해당 월의 전체 매출 합계

## 🔒 보안
- 개인정보는 환경 변수로 관리
- 인증 파일은 .gitignore로 보호
- 로그 파일에 민감한 정보 기록 금지

## 📝 로그
- 로그 파일 위치: `logs/automation.log`
- 로그 레벨: INFO
- 로그 보관 기간: 30일

## 🧪 테스트
```bash
pytest tests/
```

## 📞 지원
문제가 발생하면 로그 파일을 확인하거나 이슈를 등록해주세요. 