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

...

# Função para levar a pagina de cadastro
@app.route('/cliente_cadastro')
def ir():
    return render_template('cliente_cadastro.html')

...

# Função para cadastrar o cliente no banco de dados
@app.route('/cadastrar_cliente', methods=['POST', 'GET'])
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
        resposta = "E-mail ou Telefone já existente!"
        return render_template('confirmacao.html', resposta= resposta)     
        
    else:
        #inserindo no Banco de dados
        cursor.execute("insert into tbl_cliente (nome, idade, email, endereco, telefone) VALUES ('%s', '%s', '%s', '%s', '%s')"%( nome,idade,mail,endereco,tel))
        conn.commit()
        return render_template('confirmacao.html', resposta= nome)

...

# Função para levar a pagina de busca iniciando com uma lista geral de clientes
@app.route('/listar_clientes', methods=['GET'])
def buscar():
    conn = mysql.connect()
    cursor = conn.cursor()
    # Consultar e obter os dados dos clientes
    cursor.execute("SELECT * FROM tbl_cliente")
    lista = cursor.fetchall()
    conn.commit()   

    return render_template('busca_cliente.html', clientes = lista)

...

# Função para levar a pagina de edição do cadastro do cliente no banco de dados
@app.route('/dados_cliente', methods=['POST'])  
def dados():
    codigo = request.form.get('cod')
    conn = mysql.connect()
    cursor = conn.cursor()  
    # Buscar o registro da pessoa na tabela pelo telefone
    cursor.execute ("SELECT * FROM tbl_cliente WHERE usuario_id=%s",(codigo))   
    cli = cursor.fetchone()
    conn.commit() 
    return render_template('editar_cliente.html', cliente = cli)

...

# Função para editar o cadastro do cliente no banco de dados
@app.route('/edita_cliente', methods=['POST'])
def editar():
    id = request.form.get('cod')
    nome = request.form.get('nome')
    mail = request.form.get('email')
    tel = request.form.get('fone')
    endereco = request.form.get('end')
    idade = request.form.get('idade')
    print(id, nome, mail, tel, endereco, idade)
    conn = mysql.connect()
    cursor = conn.cursor()

    #buscando email e telefone para verificação
    valida_email = cursor.execute ('select * from tbl_cliente where email =%s', (mail)) 
    valida_telefone = cursor.execute ('select * from tbl_cliente where telefone =%s', (tel))      
    #verificando email e telefone
    if valida_email >0 or valida_telefone>0:
        resposta = "E-mail ou Telefone já existente!"
        return render_template('confirmacao.html', resposta= resposta)     
        
    else:
        #editando o cliente no Banco de dados 
        cursor.execute('UPDATE tbl_cliente SET nome = %s, idade = %s, email = %s, endereco = %s, telefone = %s  WHERE usuario_id = %s',(nome,idade,mail,endereco,tel,id))
        conn.commit()
        resposta = "Cliente editado com sucesso!"
        return render_template('confirmacao.html', resposta=resposta)

...

# Função para excluir o cadastro do cliente no banco de dados
@app.route('/exclui_cliente', methods=['POST'])
def excluir():
    tel = request.form.get('fone')
    conn = mysql.connect()
    cursor = conn.cursor()
    # Consultar e obter os dados dos clientes
    cursor.execute('DELETE FROM tbl_cliente WHERE telefone = %s',(tel))
    conn.commit()
    resposta = "Cliente excluido"

    return render_template('confirmacao.html', resposta= resposta) 

...

@app.route('/busque_cliente', methods=['POST'])
def busca():
    fone = str(request.form.get("telefone"))
    conn = mysql.connect()
    cursor = conn.cursor()
    #Consulta na tabela de Clientes
    cursor.execute("SELECT * FROM tbl_cliente WHERE telefone=%s",(fone))
    lista = cursor.fetchall()
    conn.commit()   

    return render_template('busca_cliente.html', clientes = lista)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)