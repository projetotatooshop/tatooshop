from app import app
from flask import  render_template, json, request, redirect, url_for
from pprint import pprint
from flaskext.mysql import MySQL

#conexao com DB
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'senha123'
app.config['MYSQL_DATABASE_DB'] = 'tatoo_shop'
app.config['MYSQL_DATABASE_HOST'] = 'db'

mysql = MySQL(app)

mysql.init_app(app)

# Função para levar a pagina de cadastro
@app.route('/produto_cadastro')
def produto_cadastro():
    return render_template('produto_cadastro.html')

...

# Função para cadastrar o produto no banco de dados
@app.route('/cadastrar_produto', methods=['POST', 'GET'])
def cadastrar_produto():
    pprint(request.form)
    nome = request.form.get('nome')
    marca = request.form.get('marca')
    descricao = request.form.get('descricao')
    quantidade = request.form.get('quantidade')

    conn = mysql.connect()
    cursor = conn.cursor()

    #inserindo no Banco de dados
    cursor.execute("insert into tbl_produtos (nome, marca, descricao, quantidade) VALUES ('%s', '%s', '%s', '%s')"%( nome,marca,descricao,quantidade))
    conn.commit()
    return render_template('confirmacao.html', resposta= nome)

...

# Função para levar a pagina de busca iniciando com uma lista geral de produtos
@app.route('/listar_produtos', methods=['GET'])
def listar_produtos():
    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar e obter os dados dos clientes
    cursor.execute("SELECT * FROM tbl_produtos")
    lista = cursor.fetchall()
    conn.commit()   

    return render_template('buscar_produtos.html', produtos = lista)

...

# Função para levar a pagina de edição do cadastro do produtos no banco de dados
@app.route('/dados_produtos', methods=['POST'])  
def dados_produtos():
    codigo = request.form.get('cod')
    conn = mysql.connect()
    cursor = conn.cursor()  

    # Buscar o registro do produto na tabela pelo codigo
    cursor.execute ("SELECT * FROM tbl_produtos WHERE produto_id=%s",(codigo))   
    prod = cursor.fetchone()
    conn.commit() 
    return render_template('editar_produto.html', produto = prod)

...

# Função para editar os dados do produto no banco de dados
@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    id = request.form.get('cod')
    nome = request.form.get('nome')
    marca = request.form.get('marca')
    descricao = request.form.get('descricao')
    quantidade = request.form.get('quantidade')
    print(id, nome, marca, descricao, quantidade)
    conn = mysql.connect()
    cursor = conn.cursor()

    #editando o produto no Banco de dados 
    cursor.execute('UPDATE tbl_produtos SET nome = %s, marca = %s, descricao = %s, quantidade = %s  WHERE produto_id = %s',(nome,marca,descricao,quantidade,id))
    conn.commit()
    resposta = "Produto editado com sucesso!"
    return render_template('confirmacao.html', resposta=resposta)

...

# Função para excluir o cadastro do produto no banco de dados
@app.route('/excluir_produto', methods=['POST'])
def excluir_produto():
    codigo = request.form.get('cod')
    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar e obter os dados do produto
    cursor.execute('DELETE FROM tbl_produtos WHERE produto_id = %s',(codigo))
    conn.commit()
    resposta = "Produto excluido"

    return render_template('confirmacao.html', resposta= resposta) 

...

@app.route('/buscar_produto', methods=['POST'])
def buscar_produto():
    nome = request.form.get("nome")
    conn = mysql.connect()
    cursor = conn.cursor()

    #Consulta na tabela de Produtos
    cursor.execute("SELECT * FROM tbl_produtos WHERE nome = %s",(nome))
    lista = cursor.fetchall()
    conn.commit()   

    return render_template('buscar_produtos.html', produtos = lista)
