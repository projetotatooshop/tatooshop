from flask import Flask, render_template, request, session, redirect, url_for
from app import app
from flaskext.mysql import MySQL

#conexao com DB
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'senha123'
app.config['MYSQL_DATABASE_DB'] = 'tatoo_shop'
app.config['MYSQL_DATABASE_HOST'] = 'db'

mysql = MySQL(app)

mysql.init_app(app)

@app.route('/')
def login():
    return render_template('login.html')

...

@app.route('/autenticar', methods=['POST'])
def autenticar():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    username = request.form['usuario']
    senha = request.form['senha']
    
    # Consulta para verificar se o username existe no banco
    cursor.execute("SELECT senha FROM tbl_cliente WHERE username = %s", (username,))
    resultado = cursor.fetchone()  # Retorna uma tupla com a senha, se o usuário existir
    
    if resultado:  # Se o usuário existir
        senha_banco = resultado[0]  # A senha está no primeiro elemento da tupla
        if senha == senha_banco:  # Verifica se a senha digitada corresponde à senha do banco
            session['usuario_logado'] = username
            return redirect(url_for('index'))
    
    # Se o usuário não existir ou a senha estiver incorreta
    return redirect(url_for('login', mensagem='Erro'))

...

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect(url_for('login'))