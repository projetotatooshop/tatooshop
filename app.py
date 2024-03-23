import os
from flask import Flask, render_template, json, request
from pprint import pprint
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

#conexao com DB
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'senha123'
app.config['MYSQL_DATABASE_DB'] = 'tatoo_shop'
app.config['MYSQL_DATABASE_HOST'] = 'db'

mysql.init_app(app)



@app.route('/')
def main():
    return render_template('index.html')

@app.route('/cliente_cadastro')
def ir():
    return render_template('cliente_cadastro.html')


@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
    pprint(request.form)
    nome = request.form.get('nome')
    mail = request.form.get('email')
    tel = request.form.get('fone')
    endereco = request.form.get('end')
    idade = request.form.get('idade')

    
    conn = mysql.connect()
    cursor = conn.cursor()
    #buscando email e telefone para verificação
    valida_email = cursor.execute ('select * from tbl_cliente where email =%s', (mail)) 
    valida_telefone = cursor.execute ('select * from tbl_cliente where telefone =%s', (tel))      
    #verificando email e telefone
    if valida_email >0 or valida_telefone>0:
        reposta = "E-mail ou Telefone já existente!"
        return render_template('confirmacao.html', user= reposta)     
        
    else:
        #inserindo no Banco de dados
        cursor.execute("insert into tbl_cliente (nome, idade, email, endereco, telefone) VALUES ('%s', '%s', '%s', '%s', '%s')"%( nome,idade,mail,endereco,tel))
        conn.commit()
        return render_template('confirmacao.html', user= nome)






if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)