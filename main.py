import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime

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
    for row in rows:
        cols = row.find_all('td')
        stock = cols[0].text.strip()
        support_price = cols[1].text.strip()
        signal_price = cols[2].text.strip()
        date = cols[3].text.strip()

        if stock in STOCK_LIST:
            stock_signals.append({
                "stock": stock,
                "support_price": support_price,
                "signal_price": signal_price,
                "date": date
            })

    return stock_signals

def send_email(stock_signals, from_address, to_address, password, smtp_server, smtp_port=587):
    if not stock_signals:
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

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())

if __name__ == "__main__":
    EMAIL_USER = os.environ['EMAIL_USER']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    SMTP_SERVER = os.environ['SMTP_SERVER']
    TO_EMAIL = os.environ['TO_EMAIL']
    URL = "https://www.matematikrehberim.com/dipavcisi/agresifhissesignal.php"

    stock_signals = scrape_data(URL)
    send_email(stock_signals, EMAIL_USER, TO_EMAIL, EMAIL_PASSWORD, SMTP_SERVER)