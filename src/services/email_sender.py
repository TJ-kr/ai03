import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from ..config.settings import Settings
from ..utils.logger import get_logger

class EmailSender:
    def __init__(self):
        self.logger = get_logger()
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, subject, content, recipients=None, attachments=None):
        """이메일 발송"""
        try:
            if recipients is None:
                recipients = Settings.EMAIL_RECIPIENTS
            
            # 이메일 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = Settings.EMAIL_SENDER
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # 본문 추가
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 첨부파일 추가
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)
            
            # SMTP 서버 연결 및 발송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(Settings.EMAIL_SENDER, Settings.EMAIL_PASSWORD)
                
                text = msg.as_string()
                server.sendmail(Settings.EMAIL_SENDER, recipients, text)
            
            self.logger.info(f"이메일 발송 완료: {len(recipients)}명에게 발송")
            return True
            
        except Exception as e:
            self.logger.error(f"이메일 발송 실패: {str(e)}")
            raise
    
    def _attach_file(self, msg, file_path):
        """파일 첨부"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.split("/")[-1]}'
            )
            
            msg.attach(part)
            self.logger.info(f"파일 첨부 완료: {file_path}")
            
        except Exception as e:
            self.logger.error(f"파일 첨부 실패: {str(e)}")
    
    def send_html_email(self, subject, html_content, recipients=None, attachments=None):
        """HTML 이메일 발송"""
        try:
            if recipients is None:
                recipients = Settings.EMAIL_RECIPIENTS
            
            # 이메일 메시지 생성
            msg = MIMEMultipart('alternative')
            msg['From'] = Settings.EMAIL_SENDER
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # HTML 본문 추가
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 첨부파일 추가
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)
            
            # SMTP 서버 연결 및 발송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(Settings.EMAIL_SENDER, Settings.EMAIL_PASSWORD)
                
                text = msg.as_string()
                server.sendmail(Settings.EMAIL_SENDER, recipients, text)
            
            self.logger.info(f"HTML 이메일 발송 완료: {len(recipients)}명에게 발송")
            return True
            
        except Exception as e:
            self.logger.error(f"HTML 이메일 발송 실패: {str(e)}")
            raise
    
    def test_connection(self):
        """이메일 연결 테스트"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(Settings.EMAIL_SENDER, Settings.EMAIL_PASSWORD)
            
            self.logger.info("이메일 연결 테스트 성공")
            return True
            
        except Exception as e:
            self.logger.error(f"이메일 연결 테스트 실패: {str(e)}")
            return False 