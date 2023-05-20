import time
import tkinter as tk
import io
import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from reportlab.pdfgen import canvas
 
def enviar_email():
    # Função para enviar o e-mail
 
    aluno = {
        'nome': entry_nome.get(),
        'email': entry_email.get(),
        'telefone': entry_telefone.get(),
        'data_nascimento': entry_data_nascimento.get(),
        'qualAno': entry_qual_ano.get()
    }
 
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
 
    
    # Informações sobre o envio do e-mail
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
    msg['To'] = entry_email_destino.get()
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
 
    server.sendmail(email_from, entry_email_destino.get(), msg.as_string())
    server.quit()
 
    print("E-mail enviado com sucesso!")

    time.sleep(2)

    limpar_campos()
 
# Criar a janela

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_qual_ano.delete(0, tk.END)
    entry_email_destino.delete(0, tk.END)


janela = tk.Tk()
janela.title("Formulário de Dados do Aluno")
janela.geometry("400x400")  # Define as dimensões da janela

 
# Criar os rótulos e entradas de texto
label_nome = tk.Label(janela, text="Nome Completo:", foreground="blue", font=("Arial", 12, "bold"))
label_nome.pack()
entry_nome = tk.Entry(janela, width=30,  font=("Arial", 12))
entry_nome.pack()

label_telefone = tk.Label(janela, text="Telefone:", foreground="blue", font=("Arial", 12, "bold"))
label_telefone.pack()
entry_telefone = tk.Entry(janela, width=30, font=("Arial", 12))
entry_telefone.pack()

label_data_nascimento = tk.Label(janela, text="Data de Nascimento:", foreground="blue", font=("Arial", 12, "bold"))
label_data_nascimento.pack()
entry_data_nascimento = tk.Entry(janela, width=30, font=("Arial", 12))
entry_data_nascimento.pack()

label_qual_ano = tk.Label(janela, text="Qual Ano:", foreground="blue", font=("Arial", 12, "bold"))
label_qual_ano.pack()
entry_qual_ano = tk.Entry(janela, width=30, font=("Arial", 12))
entry_qual_ano.pack()

label_email = tk.Label(janela, text="Email:", foreground="blue", font=("Arial", 12, "bold"))
label_email.pack()
entry_email = tk.Entry(janela, width=30, font=("Arial", 12))
entry_email.pack()

label_email_destino = tk.Label(janela, text="Email destinário:", foreground="blue", font=("Arial", 12, "bold"))
label_email_destino.pack()
entry_email_destino = tk.Entry(janela, width=30, font=("Arial", 12))
entry_email_destino.pack()
 
# Botão de envio
botao_enviar = tk.Button(janela, text="Enviar", command=enviar_email)
botao_enviar.pack()
 
# Iniciar a janela principal
janela.mainloop()
