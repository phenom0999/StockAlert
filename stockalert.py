from datetime import date
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class stockalert():
    def __init__(self, currentunits, contributed, datebuy, Rl=1, Ru=100, Il=8, Iu=15):
        self.Rl = Rl
        self.Ru = Ru
        self.Il = Il 
        self.Iu = Iu 
        self.currentunits = currentunits
        self.contributed = contributed
        self.datebuy = datebuy
    
    def getR(self):
        datetoday = date.today()
        return (datetoday - self.datebuy).days

    def getI(self):
        # Use the API here
        self.ticker = yf.Ticker("NDQ.AX")
        I = ((self.ticker.fast_info["lastPrice"] * self.currentunits) - self.contributed) * 100 / self.contributed 
        return round(I, 4)

    def getIdealRforI(self, I):
        Rideal = ((self.Ru - self.Rl) * (I - self.Il) / (self.Iu - self.Il)) + (self.Rl)
        return Rideal

    def alert(self):
        Rideal = self.getIdealRforI(self.getI())
        R = self.getR()
        if R > Rideal:
            return True
        return False
    
def send_email(subject, body, to_email):
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())


def main():
    datebuy = date(2025, 8, 11)
    s = stockalert(76, 3652.99, datebuy)
    if s.alert():
        subject = "Stock Alert Triggered!"
        body = f"NDQ.AX hit the alert condition.\n\nR={s.getR()}, IdealR={s.getIdealRforI(s.getI()):.2f}, I={s.getI()}%"
        send_email(subject, body, os.getenv("EMAIL_USER"))
        print("Email sent.")
    else:
        print("✅ No alert.")


if __name__ == "__main__":
    main()
