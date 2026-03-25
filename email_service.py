import smtplib
from email.message import EmailMessage

def enviar_email(arquivo, destinatario):
    email = EmailMessage()
    email["Subject"] = "Relatório de Produtos"
    email["From"] = "leonardo.tanaka07@gmail.com"
    email["To"] = destinatario

    email.set_content("Segue o relatório em anexo.")

    # anexo
    with open(arquivo, "rb") as f:
        file_data = f.read()
        file_name = f.name

    email.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    # envio
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("leonardo.tanaka07@gmail.com", "cbpg vdst gdry lljx")
        smtp.send_message(email)