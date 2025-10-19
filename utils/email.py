import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

FROM = "from.email@mail.com"
APP_PASS = "app_password"
TO = "to.email@mail.com"
SUBJECT = "Test email"
BODY = "This is a test."

msg = EmailMessage()
msg["From"] = FROM
msg["To"] = TO
msg["Subject"] = SUBJECT
msg.set_content(BODY)

# attach a file (optional)
# path = "path/to/file.pdf"
# with open(path, "rb") as f:
#     data = f.read()
#     msg.add_attachment(data, maintype="application", subtype="octet-stream", filename="file.pdf")

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(FROM, APP_PASS)
    s.send_message(msg)

print("sent")
