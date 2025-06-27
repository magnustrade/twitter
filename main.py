# author: @dipavcisi0007
# source: https://x.com/dipAVCISI007/status/1894070221469577311
# edited by: @therkut
# BIST Pay Endeksleri 
# **** Katılım ****

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime, timedelta

def load_stock_list(file_path="data/stock.txt"):
    """stock.txt dosyasından hisse listesini yükler (her satır bir hisse)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            stock_list = [line.strip().strip(',') for line in file.readlines() if line.strip()]
            return stock_list
    except FileNotFoundError:
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return []
    except Exception as e:
        print(f"Hata: Dosya okunurken bir sorun oluştu: {e}")
        return []

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Skip the header row

    stock_signals = []
    today = datetime.now()
    business_days_count = 0
    days_back = 0
    three_business_days_ago = None

    while business_days_count < 3:
        current_date = today - timedelta(days=days_back)
        if current_date.weekday() < 5:  # Cumartesi (5) ve Pazar (6) hariç
            business_days_count += 1
        days_back += 1
    three_business_days_ago = today - timedelta(days=days_back)

    STOCK_LIST = load_stock_list()

    for row in rows:
        cols = row.find_all('td')
        stock = cols[0].text.strip()
        support_price = cols[1].text.strip()
        signal_price = cols[2].text.strip()
        date_str = cols[4].text.strip()

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            if date >= three_business_days_ago:
                if stock in STOCK_LIST:
                    stock_signals.append({
                        "stock": stock,
                        "support_price": support_price,
                        "signal_price": signal_price,
                        "date": date_str
                    })
        except ValueError as e:
            print(f"Tarih formatı hatalı: {date_str}, hata: {e}")
            continue

    return stock_signals

def is_valid_email(email):
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return False
    return True

def send_email(stock_signals, from_name, from_address, to_addresses, password, smtp_server="smtp.gmail.com", smtp_port=465):
    if not stock_signals:
        print("Gönderilecek sinyal yok.")
        return

    if not all([from_address, to_addresses, password, smtp_server]):
        print("Hata: E-posta bilgileri eksik.")
        return

    valid_to_addresses = [email for email in to_addresses if is_valid_email(email)]
    if not valid_to_addresses:
        print("Hata: Hiçbir geçerli alıcı adresi bulunamadı.")
        return

    invalid_addresses = set(to_addresses) - set(valid_to_addresses)
    if invalid_addresses:
        print(f"Geçersiz e-posta adresleri tespit edildi ve hariç tutuldu: {invalid_addresses}")

    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")  # Sadece tarih, saat yok
    current_year = now.strftime("%Y")

    html_body = f"""
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:600px; margin:0 auto; background-color:#ffffff; border-radius:8px;">
        <tbody>
            <tr>
                <td style="padding:25px; text-align:center;">
                    <h2 style="margin:0; font-size:24px; color:#333;">Engulfing Candles Tarama {date_str}</h2>
                </td>
            </tr>
            <tr>
                <td style="padding:20px;">
                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;">
                        <tbody>
                            <tr style="background-color:#f5f5f5;">
                                <th style="padding:12px 8px; border:1px solid #e0e0e0; font-size:12px; font-weight:600; color:#2c3e50;">Hisse</th>
                                <th style="padding:12px 8px; border:1px solid #e0e0e0; font-size:12px; font-weight:600; color:#2c3e50;">Destek Fiyatı</th>
                                <th style="padding:12px 8px; border:1px solid #e0e0e0; font-size:12px; font-weight:600; color:#2c3e50;">Signal Fiyatı</th>
                                <th style="padding:12px 8px; border:1px solid #e0e0e0; font-size:12px; font-weight:600; color:#2c3e50;">Tarih</th>
                            </tr>
    """

    for i, signal in enumerate(stock_signals):
        row_bg = "#f8f9fa" if i % 2 == 0 else "#ffffff"
        html_body += f"""
                            <tr style="background-color:{row_bg};">
                                <td style="padding:12px 8px; border:1px solid #e0e0e0; text-align:center;"><strong>{signal['stock']}</strong></td>
                                <td style="padding:12px 8px; border:1px solid #e0e0e0; text-align:center;">{signal['support_price']}</td>
                                <td style="padding:12px 8px; border:1px solid #e0e0e0; text-align:center;">{signal['signal_price']}</td>
                                <td style="padding:12px 8px; border:1px solid #e0e0e0; text-align:center;">{signal['date']}</td>
                            </tr>
        """

    html_body += f"""
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding:20px;">
                    <div style="background-color:#fff3e0; padding:15px; border-radius:8px; text-align:center; color:#e65100; font-size:13px; font-weight:600;">
                        ⚠️ YASAL UYARI: Bu rapor bilgilendirme amaçlıdır, yatırım tavsiyesi içermez.
                    </div>
                </td>
            </tr>
            <tr>
                <td style="background-color:#f5f5f5; padding:20px; text-align:center; border-top:1px solid #e0e0e0;">
                    <p style="margin:0 0 10px 0;font-size:12px;color:#666;">Bu liste BIST Katılım Pay Endeksine göre filtrelenmiştir.</p>
                    <p style="margin:0 0 10px 0; font-size:12px; color:#666;">Bu e-posta otomatik olarak gönderilmiştir. Lütfen yanıt vermeyiniz.</p>
                    <p style="margin:0; font-size:12px; color:#666;">Author: @dipavcisi0007 © {current_year} Edited by Magnus Trade</p>
                </td>
            </tr>
        </tbody>
    </table>
    """

    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_address}>"
    msg['To'] = ", ".join(valid_to_addresses)
    msg['Subject'] = "📊 Agresif Hisse Taraması Günlük Sinyalleri"
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(from_address, password)
            server.sendmail(from_address, valid_to_addresses, msg.as_string())
        print("E-posta başarıyla gönderildi!")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"Hata: Alıcı adresleri reddedildi: {e.recipients}")
    except smtplib.SMTPAuthenticationError:
        print("Hata: Kimlik doğrulama başarısız. E-posta veya şifre yanlış olabilir.")
    except Exception as e:
        print(f"Hata oluştu: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    TO_EMAIL = os.environ.get('TO_EMAIL')
    SCRAPE_URL = os.environ.get('SCRAPE_URL')
    FROM_NAME = "Magnus Trade"

    if not all([EMAIL_USER, EMAIL_PASSWORD, SMTP_SERVER, TO_EMAIL, SCRAPE_URL]):
        print("Hata: Ortam değişkenlerinden biri eksik.")
    else:
        to_email_list = [email.strip() for email in TO_EMAIL.split(',')]
        print(f"TO_EMAIL listesi: {to_email_list}")
        stock_signals = scrape_data(SCRAPE_URL)
        send_email(stock_signals, FROM_NAME, EMAIL_USER, to_email_list, EMAIL_PASSWORD, SMTP_SERVER)
