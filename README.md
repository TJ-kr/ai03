# 자판기 매출 관리 시스템

자동으로 웹사이트에서 매출 데이터를 다운로드하고, 구글 스프레드시트에 저장한 후 이메일로 보고서를 발송하는 시스템입니다.

## 📊 프로젝트 진행 상황

현재 프로젝트의 진행 상황을 확인하려면:

```bash
# 프로젝트 대시보드 확인
python scripts/project_dashboard.py

# 마일스톤 상태 확인
python scripts/update_milestone.py show
```

자세한 마일스톤 정보는 [MILESTONES.md](MILESTONES.md) 파일을 참조하세요.

## 주요 기능

1. **웹사이트 자동 로그인 및 파일 다운로드**
   - 지정된 웹사이트에 자동 로그인
   - 매출 데이터 파일 자동 다운로드

2. **구글 스프레드시트 자동 업데이트**
   - 다운로드된 데이터를 'main' 시트에 자동 추가
   - 중복 데이터 방지 기능

3. **자동 이메일 보고서 발송**
   - 일일 매출 요약
   - 재고 현황
   - 월 누적 매출
   - 상세 매출 데이터 테이블

## 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정
```bash
cp env.example .env
```
`.env` 파일을 편집하여 필요한 정보를 입력하세요.

### 3. 구글 API 인증 설정
1. Google Cloud Console에서 프로젝트 생성
2. Google Sheets API 활성화
3. 서비스 계정 생성 및 JSON 키 파일 다운로드
4. `credentials.json` 파일을 프로젝트 루트에 저장
5. 구글 스프레드시트에 서비스 계정 이메일 공유 권한 부여

## 사용법

### 기본 실행
```bash
# 즉시 실행
python src/main.py

# 스케줄러 모드 (매일 09:00 실행)
python src/main.py --schedule

# 연결 테스트
python src/main.py --test
```

### 프로젝트 관리
```bash
# 프로젝트 대시보드 확인
python scripts/project_dashboard.py

# 프로젝트 상태 점검
python scripts/project_dashboard.py --health

# 마일스톤 상태 확인
python scripts/update_milestone.py show

# 마일스톤 업데이트
python scripts/update_milestone.py update 2 완료 100 '웹사이트 자동화 완성'
```

## 프로젝트 구조

```
vending_machine_automation/
├── src/                    # 소스 코드
│   ├── main.py            # 메인 실행 파일
│   ├── config/            # 설정 파일들
│   ├── services/          # 핵심 서비스들
│   ├── utils/             # 유틸리티 함수들
│   └── templates/         # 이메일 템플릿
├── scripts/               # 프로젝트 관리 스크립트
│   ├── project_dashboard.py    # 프로젝트 대시보드
│   └── update_milestone.py     # 마일스톤 업데이트
├── logs/                  # 로그 파일들
├── downloads/             # 다운로드된 파일들
├── MILESTONES.md          # 마일스톤 관리 문서
└── credentials.json       # 구글 API 인증 파일
```

## 설정 항목

- `WEBSITE_URL`: 데이터를 다운로드할 웹사이트 URL
- `WEBSITE_USERNAME`: 웹사이트 로그인 아이디
- `WEBSITE_PASSWORD`: 웹사이트 로그인 비밀번호
- `EMAIL_SENDER`: 발송자 이메일 주소
- `EMAIL_PASSWORD`: 발송자 이메일 비밀번호 (앱 비밀번호 권장)
- `EMAIL_RECIPIENTS`: 수신자 이메일 주소들 (쉼표로 구분)

## 마일스톤 관리

이 프로젝트는 체계적인 마일스톤을 통해 개발됩니다:

1. **마일스톤 1**: 기본 구조 및 설정 ✅ 완료
2. **마일스톤 2**: 웹사이트 자동화 구현 🔄 진행중
3. **마일스톤 3**: 구글 스프레드시트 연동 테스트 ⏳ 대기
4. **마일스톤 4**: 이메일 시스템 구현 ⏳ 대기
5. **마일스톤 5**: 통합 테스트 및 디버깅 ⏳ 대기
6. **마일스톤 6**: 스케줄링 및 배포 ⏳ 대기
7. **마일스톤 7**: 문서화 및 최종 검증 ⏳ 대기
8. **마일스톤 8**: GitHub 배포 및 릴리즈 ⏳ 대기

자세한 내용은 [MILESTONES.md](MILESTONES.md) 파일을 참조하세요.

## 주의사항

- 이메일 비밀번호는 Gmail의 경우 앱 비밀번호를 사용하세요
- 구글 스프레드시트에 서비스 계정의 공유 권한을 반드시 부여하세요
- 로그 파일을 정기적으로 확인하여 오류를 점검하세요
- 웹사이트 구조 변경 시 `web_scraper.py` 파일을 수정해야 할 수 있습니다

## 기여하기

1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요. 