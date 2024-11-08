import smtplib
from app.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email: str, code: str):
    from_email = settings.EMAIL_SMTP
    from_password = settings.PASSWORD_SMTP

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Verification Code"

    body = f"Ваш код подтверждения: {code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
