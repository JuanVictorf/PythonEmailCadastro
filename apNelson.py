import smtplib
from email.mime.text import MIMEText

# Função para enviar o e-mail
def enviar_email(aluno, email_destino):
    
    email_from = 'canaldojuan59@gmail.com'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_from, 'ymqfkwyyyhtnaqyl')

    subject = f"Novo cadastro de aluno: {aluno['nome']}"
    body = f"Nome: {aluno['nome']}\nEmail: {aluno['email']}\nTelefone: {aluno['telefone']}\nData de Nascimento: {aluno['data_nascimento']}\nQual Ano: {aluno['qualAno']}"

    msg = f'Subject: {subject} \n\n{body}'

    server.sendmail(email_from, email_destino, msg)
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