import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from .templates import create_sales_report_email, create_simple_text_email

# 환경 변수 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

def send_sales_report_email(report_data, attachment_path=None):
    """매출 보고서 이메일을 발송합니다."""
    
    # 이메일 설정
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_emails = os.getenv('RECIPIENT_EMAILS', '').split(',')
    
    if not all([sender_email, sender_password, recipient_emails]):
        print("이메일 설정이 완료되지 않았습니다. .env 파일을 확인하세요.")
        return False
    
    try:
        # 이메일 메시지 생성
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipient_emails)
        msg['Subject'] = f"자판기 매출 보고서 - {report_data['report_date'][:10]}"
        
        # HTML 이메일 생성
        html_content = create_sales_report_email(report_data)
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 텍스트 이메일 생성 (대체)
        text_content = create_simple_text_email(report_data)
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 첨부파일 추가 (엑셀 파일)
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path)}'
            )
            msg.attach(part)
        
        # 이메일 발송
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_emails, text)
        server.quit()
        
        print(f"이메일 발송 성공: {len(recipient_emails)}명에게 발송")
        return True
        
    except Exception as e:
        print(f"이메일 발송 실패: {e}")
        return False 