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
    "BINHO", "AVOD", "ACSEL", "ADESE", "AFYON", "AHSGY", "AKCNS", "AKFYE", "ATEKS", "AKSA", "AKSEN", "ALBRK", "ALCTL",
    "ALKA", "ALKIM", "ALTNY", "ALKLC", "ALVES", "ASUZU", "ANELE", "ARDYZ", "ARENA", "ARTMS", "ASGYO", "ASELS", "ATAGY",
    "ATAKP", "ATATP", "AVPGY", "AYEN", "BAKAB", "BNTAS", "BANVT", "BARMA", "BASGZ", "BEGYO", "BAYRK", "BRKSN", "BEYAZ",
    "BIENY", "BIMAS", "BIOEN", "BRLSM", "BMSTL", "BOBET", "BORSK", "BORLS", "BOSSA", "BURCE", "BURVA", "BUCIM", "CANTE",
    "CATES", "CLEBI", "CEMAS", "CEMTS", "CMBTN", "CIMSA", "CCOLA", "COSMO", "CUSAN", "CWENE", "DAPGM", "DARDL", "DGATE",
    "DCTTR", "DESA", "DESPC", "DITAS", "DOFER", "DGNMO", "ARASE", "DGGYO", "DOAS", "DOGUB", "DURKN", "DYOBY", "EBEBK",
    "EFORC", "EGGUB", "EGPRO", "EKOS", "EKSUN", "ELITE", "ENJSA", "ERCB", "EREGL", "ERSU", "ESCOM", "TEZOL", "EUPWR",
    "EYGYO", "FADE", "FMIZP", "FONET", "FORMT", "FRIGO", "FZLGY", "GEDZA", "GENIL", "GENTS", "GEREL", "GMTAS", "GESAN",
    "GOLTS", "GRTRK", "GUBRF", "GUNDG", "GRSEL", "HRKET", "HATSN", "HKTM", "HUBVC", "HUNER", "ICUGS", "IDGYO", "IHEVA",
    "IHGZT", "IHYAY", "IMASM", "INGRM", "INTEM", "ISSEN", "ISKPL", "IEYHO", "ISDMR", "IZINV", "IZFAS", "JANTS", "KFEIN",
    "KLKIM", "KRDMA", "KRDMB", "KRDMD", "KAREL", "KARSN", "KRTEK", "KARYE", "KTLEV", "KATMR", "KAYSE", "KRVGD", "TCKRC",
    "KZBGY", "KOCMT", "KCAER", "KNFRT", "KONTR", "KONYA", "KONKA", "KGYO", "KRGYO", "KRPLS", "KOTON", "KOPOL", "KRSTL",
    "KRONT", "KUTPO", "KUYAS", "KBORU", "LILAK", "LMKDC", "LINK", "LOGO", "LKMNH", "LYDHO", "MAKIM", "MAKTK", "MANAS",
    "MTRKS", "MAVI", "MEDTR", "MEGMT", "MEKAG", "MNDRS", "MERCN", "MERKO", "MIATK", "MPARK", "MOBTL", "MNDTR", "EGEPO",
    "NTGAZ", "NETAS", "NIBAS", "NUHCM", "NUGYO", "OBAMS", "ODAS", "OFSYM", "ONCSM", "ONRYT", "ORCAY", "ORGE", "OTKAR",
    "OYAKC", "OZATD", "OZRDN", "OZSUB", "OZYSR", "PAGYO", "PRDGS", "PARSN", "PASEU", "PATEK", "PGSUS", "PEKGY", "PENGD",
    "PENTA", "PETKM", "PETUN", "PNSUT", "PKART", "PLTUR", "POLHO", "QUAGR", "RALYH", "RYGYO", "RODRG", "RUBNS", "SAFKR",
    "SANEL", "SNICA", "SANFM", "SANKO", "SAMAT", "SASA", "SEGMN", "SEKUR", "SELEC", "SELGD", "SELVA", "SRVGY", "SILVR",
    "SNGYO", "SMRTG", "SMART", "SOKE", "SONME", "SUNTK", "SURGY", "SUWEN", "TABGD", "TKFEN", "TDGYO", "TUCLK", "TUKAS",
    "TMSN", "TUPRS", "TUREX", "MARBL", "THYAO", "TRILC", "PRKAB", "TURGG", "ULUSE", "USAK", "VAKKO", "VANGD", "VBTYZ",
    "VESTL", "VESBE", "YATAS", "YEOTK", "YKSLN", "YUNSA", "ZEDUR"
]

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Skip the header row

    stock_signals = []
    # Şu anki tarihi al ve son 3 günün sınırını hesapla
    today = datetime.now()
    three_days_ago = today - timedelta(days=3)

    for row in rows:
        cols = row.find_all('td')
        stock = cols[0].text.strip()
        support_price = cols[1].text.strip()
        signal_price = cols[2].text.strip()
        date_str = cols[3].text.strip()

        # Tarih string'ini datetime objesine çevir (format: "YYYY-MM-DD HH:MM:SS")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            # Tarih son 3 gün içindeyse ekle
            if date >= three_days_ago:
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
