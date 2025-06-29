# 📧 Gmail 앱 비밀번호 설정 가이드

## 🎯 개요

TOYGO 자판기 매출 관리 시스템에서 이메일을 발송하기 위해서는 Gmail의 앱 비밀번호를 설정해야 합니다. 이 가이드는 단계별로 Gmail 앱 비밀번호를 생성하고 설정하는 방법을 설명합니다.

---

## 📋 사전 준비사항

1. **Gmail 계정**: 발송용 Gmail 계정이 필요합니다
2. **2단계 인증**: Gmail에서 2단계 인증이 활성화되어 있어야 합니다
3. **보안 설정**: 앱 비밀번호 생성을 위한 보안 설정이 필요합니다

---

## 🔧 단계별 설정 방법

### 1단계: Gmail 2단계 인증 활성화

1. **Gmail 계정에 로그인**
   - https://mail.google.com 접속
   - 발송용 Gmail 계정으로 로그인

2. **Google 계정 설정으로 이동**
   - Gmail 우측 상단의 프로필 사진 클릭
   - "Google 계정 관리" 클릭

3. **보안 탭으로 이동**
   - 좌측 메뉴에서 "보안" 클릭

4. **2단계 인증 설정**
   - "2단계 인증" 섹션에서 "2단계 인증 사용" 클릭
   - 휴대폰 번호 인증 등 필요한 설정 완료

### 2단계: 앱 비밀번호 생성

1. **앱 비밀번호 페이지로 이동**
   - Google 계정 관리 → 보안 → 2단계 인증
   - "앱 비밀번호" 클릭

2. **앱 선택**
   - "앱 선택" 드롭다운에서 "기타(맞춤 이름)" 선택
   - 앱 이름에 "TOYGO 자판기 시스템" 입력

3. **앱 비밀번호 생성**
   - "생성" 버튼 클릭
   - 16자리 앱 비밀번호가 생성됩니다 (예: `abcd efgh ijkl mnop`)

4. **앱 비밀번호 복사**
   - 생성된 16자리 비밀번호를 복사하여 안전한 곳에 보관
   - **중요**: 이 비밀번호는 한 번만 표시되므로 반드시 복사해두세요!

### 3단계: 환경변수 설정

1. **프로젝트 루트에 .env 파일 생성**
   ```bash
   # vending_machine_automation/.env
   ```

2. **이메일 설정 추가**
   ```env
   # 웹사이트 로그인 정보
   WEBSITE_URL=https://toygo.smartm.co.kr
   WEBSITE_USERNAME=locolor
   WEBSITE_PASSWORD=locolor2025

   # 구글 스프레드시트 설정
   SPREADSHEET_ID=1PckoSzEWtsxt6seKG-n8wms_00G-cTf7eNjR6Rj-ggE
   GOOGLE_CREDENTIALS_FILE=credentials.json

   # 이메일 설정
   EMAIL_SENDER=your-gmail@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop
   EMAIL_RECIPIENTS=recipient1@email.com,recipient2@email.com

   # 로그 설정
   LOG_LEVEL=INFO
   LOG_FILE=logs/vending_machine.log
   ```

3. **설정값 변경**
   - `EMAIL_SENDER`: 발송용 Gmail 주소로 변경
   - `EMAIL_PASSWORD`: 생성한 16자리 앱 비밀번호로 변경
   - `EMAIL_RECIPIENTS`: 수신자 이메일 주소들로 변경 (쉼표로 구분)

---

## 🧪 설정 확인 및 테스트

### 1. 이메일 발송 테스트 실행

```bash
cd vending_machine_automation
python scripts/test_email_sender.py
```

### 2. 예상 결과

성공적인 경우:
```
🚀 TOYGO 자판기 매출 시스템 - 이메일 발송 테스트
======================================================================

==================== 연결 테스트 ====================
📧 이메일 연결 테스트 시작
==================================================
📋 이메일 설정 확인:
   발신자: your-gmail@gmail.com
   비밀번호: ****************
   수신자: ['recipient1@email.com', 'recipient2@email.com']

🔗 SMTP 서버 연결 테스트 중...
✅ 이메일 연결 테스트 성공!

==================== 간단한 이메일 ====================
📧 간단한 이메일 발송 테스트
==================================================
📤 이메일 발송 중...
✅ 이메일 발송 완료!

==================== HTML 이메일 ====================
📧 HTML 이메일 발송 테스트
==================================================
📤 HTML 이메일 발송 중...
✅ HTML 이메일 발송 완료!

==================== 첨부파일 이메일 ====================
📧 첨부파일 이메일 발송 테스트
==================================================
📤 첨부파일 이메일 발송 중...
✅ 첨부파일 이메일 발송 완료!

======================================================================
📊 테스트 결과 요약:
   연결 테스트: ✅ 성공
   간단한 이메일: ✅ 성공
   HTML 이메일: ✅ 성공
   첨부파일 이메일: ✅ 성공

🎉 모든 이메일 테스트가 성공했습니다!
이제 실제 매출 데이터와 함께 이메일을 발송할 수 있습니다.
```

---

## ⚠️ 주의사항

### 보안 관련
1. **앱 비밀번호 보안**: 앱 비밀번호는 절대 공유하지 마세요
2. **환경변수 파일**: .env 파일은 .gitignore에 포함되어 있어야 합니다
3. **정기적 갱신**: 보안을 위해 앱 비밀번호를 정기적으로 갱신하는 것을 권장합니다

### Gmail 제한사항
1. **일일 발송 한도**: Gmail은 하루 최대 500통의 이메일 발송 제한이 있습니다
2. **스팸 필터**: 대량 발송 시 스팸으로 분류될 수 있으니 주의하세요
3. **첨부파일 크기**: 첨부파일은 25MB 이하여야 합니다

---

## 🔧 문제 해결

### 일반적인 오류 및 해결방법

#### 1. "Username and Password not accepted" 오류
- **원인**: 앱 비밀번호가 잘못되었거나 2단계 인증이 비활성화됨
- **해결**: 2단계 인증을 활성화하고 새로운 앱 비밀번호를 생성

#### 2. "SMTPAuthenticationError" 오류
- **원인**: Gmail 계정의 보안 설정 문제
- **해결**: 
  - "보안 수준이 낮은 앱의 액세스" 허용
  - 또는 앱 비밀번호를 다시 생성

#### 3. "Connection refused" 오류
- **원인**: 방화벽이나 네트워크 문제
- **해결**: 
  - 포트 587이 열려있는지 확인
  - 회사 네트워크인 경우 IT 관리자에게 문의

#### 4. "Recipient address rejected" 오류
- **원인**: 수신자 이메일 주소가 잘못됨
- **해결**: 수신자 이메일 주소를 정확히 입력

---

## 📞 추가 지원

설정 중 문제가 발생하면 다음을 확인해주세요:

1. **로그 파일 확인**: `logs/vending_machine.log` 파일에서 상세한 오류 메시지 확인
2. **Gmail 설정 재확인**: 2단계 인증과 앱 비밀번호 설정 재확인
3. **네트워크 연결**: 인터넷 연결 상태 확인

---

## ✅ 완료 체크리스트

- [ ] Gmail 2단계 인증 활성화
- [ ] 앱 비밀번호 생성 및 복사
- [ ] .env 파일에 이메일 설정 추가
- [ ] 이메일 발송 테스트 실행
- [ ] 모든 테스트 통과 확인
- [ ] 실제 수신자에게 테스트 이메일 수신 확인

모든 항목이 완료되면 이메일 시스템이 정상적으로 작동합니다! 🎉 