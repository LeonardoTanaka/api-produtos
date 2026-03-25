import smtplib
import os
from email.message import EmailMessage

def enviar_email(arquivo, destinatario):
    email = EmailMessage()
    email["Subject"] = "Relatório de Produtos"
    email["From"] = os.getenv("EMAIL_USER")
    email["To"] = destinatario

    email.set_content("Segue o relatório em anexo.")

    # anexo
    with open(arquivo, "rb") as f:
        file_data = f.read()
        file_name = f.name

    email.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=file_name
    )

    # envio (porta 587 + TLS)
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASS")
        )
        smtp.send_message(email)