import io
import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from reportlab.pdfgen import canvas

# Função para enviar o e-mail
def enviar_email(aluno, email_destino):

    # Conexão com o banco de dados MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="aluno_python"
    )
    
    cursor = db.cursor()
    
    # Inserção dos dados do aluno no banco de dados
    sql = "INSERT INTO alunos (nome, email, telefone, data_nascimento, qual_ano) VALUES (%s, %s, %s, %s, %s)"
    val = (aluno['nome'], aluno['email'], aluno['telefone'], aluno['data_nascimento'], aluno['qualAno'])
    cursor.execute(sql, val)
    
    db.commit()
    print(f"Dados do aluno {aluno['nome']} inseridos no banco de dados com sucesso!")
    
    email_from = 'canaldojuan59@gmail.com'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_from, 'ymqfkwyyyhtnaqyl')

    subject = f"Novo cadastro de aluno: {aluno['nome']}"
    body = f"Nome: {aluno['nome']}\nEmail: {aluno['email']}\nTelefone: {aluno['telefone']}\nData de Nascimento: {aluno['data_nascimento']}\nQual Ano: {aluno['qualAno']}"

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_destino
    msg['Subject'] = subject

    # Corpo do e-mail
    msg.attach(MIMEText(body, 'plain'))

    # Anexo do PDF com os dados do aluno
    pdf_data = io.BytesIO()
    pdf = canvas.Canvas(pdf_data)
    pdf.drawString(100, 750, f"Nome: {aluno['nome']}")
    pdf.drawString(100, 700, f"E-mail: {aluno['email']}")
    pdf.drawString(100, 650, f"Telefone: {aluno['telefone']}")
    pdf.drawString(100, 600, f"Data de Nascimento: {aluno['data_nascimento']}")
    pdf.drawString(100, 550, f"Qual Ano: {aluno['qualAno']}")
    pdf.save()
    pdf_data.seek(0)
    pdf_attachment = MIMEApplication(pdf_data.read(), _subtype='pdf')
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"{aluno['nome']}.pdf")
    msg.attach(pdf_attachment)

    server.sendmail(email_from, email_destino, msg.as_string())
    server.quit()

    print("E-mail enviado com sucesso!")


# Pergunta dos dados do aluno
aluno = {}
aluno['nome'] = input("Digite o nome do aluno: ")
aluno['email'] = input("Digite o e-mail do aluno: ")
aluno['telefone'] = input("Digite o telefone do aluno: ")
aluno['data_nascimento'] = input("Digite a data de nascimento do aluno: ")
aluno['qualAno'] = input("Digite qual ano o aluno está: ")

# Pergunta do e-mail de destino
email_destino = input("Digite o e-mail para onde deseja enviar o cadastro do aluno: ")

# Envio do e-mail com os dados do aluno
enviar_email(aluno, email_destino)
