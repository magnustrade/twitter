import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(from_address, to_address, password, smtp_server, smtp_port=587):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "GitHub'dan Test E-postası"
    body = "Bu e-posta GitHub Actions üzerinden gönderilmiştir."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_address, password)
            server.sendmail(from_address, to_address, msg.as_string())
        print("E-posta başarıyla gönderildi!")
    except smtplib.SMTPAuthenticationError:
        print("Hata: Kimlik doğrulama başarısız. E-posta veya şifre yanlış olabilir.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    EMAIL_USER = os.environ['EMAIL_USER']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    SMTP_SERVER = os.environ['SMTP_SERVER']
    TO_EMAIL = os.environ['TO_EMAIL']

    print(f"E-posta adresi: {EMAIL_USER}")
    print(f"SMTP sunucusu: {SMTP_SERVER}")
    print(f"Alıcı e-posta: {TO_EMAIL}")

    send_email(EMAIL_USER, TO_EMAIL, EMAIL_PASSWORD, SMTP_SERVER)
