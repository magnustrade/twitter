import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime, timedelta

# author: @dipavcisi0007
# edited by: @therkut
# BIST Pay Endeksleri 
# **** Katılım ****

STOCK_LIST = [
    "ACSEL", "ADESE", "AHSGY", "AKCNS", "AKSA", "AKSEN", "AKYHO", "ALBRK", "ALCTL", "ALKA", "ALKIM", "ALKLC", "ALTNY",
    "ALVES", "ANGEN", "ARASE", "ARDYZ", "ARENA", "ASELS", "ASUZU", "ATAKP", "ATATP", "ATEKS", "AVGYO", "AVPGY", "BAHKM",
    "BAKAB", "BANVT", "BASGZ", "BAYRK", "BERA", "BEYAZ", "BIENY", "BIMAS", "BINHO", "BMSTL", "BORLS", "BORSK", "BOSSA",
    "BRKSN", "BRLSM", "BSOKE", "BUCIM", "BURCE", "BURVA", "CANTE", "CEMAS", "CEMTS", "CMBTN", "COSMO", "CUSAN", "CWENE",
    "DAGHL", "DARDL", "DCTTR", "DESPC", "DGATE", "DGNMO", "DMRGD", "DOAS", "DOBUR", "DOFER", "DYOBY", "EBEBK", "EDATA",
    "EDIP", "EGEPO", "EGGUB", "EGPRO", "EKSUN", "ELITE", "ENJSA", "ERCB", "EREGL", "ESCOM", "ESEN", "EUPWR", "EYGYO",
    "FADE", "FMIZP", "FONET", "FORMT", "FZLGY", "GEDZA", "GENIL", "GENTS", "GEREL", "GOKNR", "GOLTS", "GOODY", "GRSEL",
    "GRTRK", "GUBRF", "GUNDG", "GWIND", "HATSN", "HKTM", "HOROZ", "HRKET", "HTTBT", "HUNER", "IDGYO", "IHEVA", "IHGZT",
    "IHLAS", "IHLGM", "IHYAY", "IMASM", "INGRM", "INTEM", "ISDMR", "ISKPL", "ISSEN", "IZFAS", "IZINV", "JANTS", "KAREL",
    "KATMR", "KAYSE", "KCAER", "KGYO", "KIMMR", "KLSYN", "KNFRT", "KONKA", "KONYA", "KOPOL", "KOTON", "KRDMA", "KRDMB",
    "KRDMD", "KRGYO", "KRONT", "KRPLS", "KRSTL", "KRVGD", "KTLEV", "KUTPO", "KUYAS", "KZBGY", "LILAK", "LKMNH", "LMKDC",
    "LOGO", "LRSHO", "LUKSK", "MAGEN", "MAKIM", "MANAS", "MARBL", "MARKA", "MAVI", "MEDTR", "MEGAP", "MEKAG", "MERCN",
    "MERKO", "MIATK", "MIPAZ", "MNDRS", "MNDTR", "MOBTL", "MPARK", "NATEN", "NETAS", "NTGAZ", "NUHCM", "OBAMS", "OBASE",
    "ONCSM", "ORCAY", "ORGE", "OSTIM", "OYAKC", "OZATD", "OZRDN", "OZSUB", "OZYSR", "PARSN", "PASEU", "PEHOL", "PEKGY",
    "PENGD", "PENTA", "PETKM", "PETUN", "PKART", "PLTUR", "PNSUT", "POLHO", "PRKAB", "QUAGR", "RALYH", "RODRG", "RUBNS",
    "SAFKR", "SAMAT", "SANKO", "SAYAS", "SEGMN", "SEKUR", "SELEC", "SELVA", "SILVR", "SMART", "SMRTG", "SNGYO", "SNICA",
    "SOKE", "SRVGY", "SUNTK", "SURGY", "SUWEN", "TCKRC", "TDGYO", "TEZOL", "TKFEN", "TNZTP", "TUCLK", "TUKAS", "TUPRS",
    "TUREX", "ULUSE", "USAK", "VAKKO", "VANGD", "VBTYZ", "VESBE", "VESTL", "YATAS", "YEOTK", "YUNSA", "ZEDUR"
]

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Skip the header row

    stock_signals = []
    # Şu anki tarihi al ve son 3 iş gününün sınırını hesapla
    today = datetime.now()
    business_days_count = 0
    days_back = 0
    three_business_days_ago = None

    while business_days_count < 3:
        current_date = today - timedelta(days=days_back)
        # Hafta içi mi kontrol et (0-4: Pazartesi-Cuma)
        if current_date.weekday() < 5:
            business_days_count += 1
        days_back += 1
    three_business_days_ago = today - timedelta(days=days_back)

    for row in rows:
        cols = row.find_all('td')
        stock = cols[0].text.strip()
        support_price = cols[1].text.strip()
        signal_price = cols[2].text.strip()
        date_str = cols[3].text.strip()

        # Tarih string'ini datetime objesine çevir (format: "YYYY-MM-DD HH:MM:SS")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            # Tarih son 3 iş günü içindeyse ekle
            if date >= three_business_days_ago:
                if stock in STOCK_LIST:
                    stock_signals.append({
                        "stock": stock,
                        "support_price": support_price,
                        "signal_price": signal_price,
                        "date": date_str  # Orijinal string formatında tutuyoruz
                    })
        except ValueError as e:
            print(f"Tarih formatı hatalı: {date_str}, hata: {e}")
            continue

    return stock_signals

def send_email(stock_signals, from_address, to_address, password, smtp_server="smtp.gmail.com", smtp_port=465):
    if not stock_signals:
        print("Gönderilecek sinyal yok.")
        return

    if not all([from_address, to_address, password, smtp_server]):
        print("Hata: E-posta bilgileri eksik.")
        return

    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y %H:%M")
    subject = "Agresif Hisse Taraması Günlük Sinyalleri"
    body = f"Engulfing Candles Tarama {date_str}\n\n"

    for signal in stock_signals:
        body += f"Hisse: {signal['stock']}\n"
        body += f"Destek Fiyatı: {signal['support_price']}\n"
        body += f"Signal Fiyatı: {signal['signal_price']}\n"
        body += f"Tarih: {signal['date']}\n\n"
        body += f"------------------------\n\n"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(from_address, password)
            server.sendmail(from_address, to_address, msg.as_string())
        print("E-posta başarıyla gönderildi!")
    except smtplib.SMTPAuthenticationError:
        print("Hata: Kimlik doğrulama başarısız. E-posta veya şifre yanlış olabilir.")
    except Exception as e:
        print(f"Hata oluştu: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    TO_EMAIL = os.environ.get('TO_EMAIL')

    if not all([EMAIL_USER, EMAIL_PASSWORD, SMTP_SERVER, TO_EMAIL]):
        print("Hata: Ortam değişkenlerinden biri eksik.")
    else:
        stock_signals = scrape_data("https://www.matematikrehberim.com/dipavcisi/agresifhissesignal.php")
        send_email(stock_signals, EMAIL_USER, TO_EMAIL, EMAIL_PASSWORD, SMTP_SERVER)
