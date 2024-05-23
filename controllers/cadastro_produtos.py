from app import app
from flask import  render_template, request, session
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
    if session['usuario_logado'] != 'admin':
        return 'Você não tem permissão para acessar essa página. <a href="/">Voltar</a>'
    
    campos = [
        {'texto': 'Nome', 'tipo': 'text', 'id': 'nome', 'nome': 'nome'},
        {'texto': 'Marca', 'tipo': 'text', 'id': 'marca', 'nome': 'marca'},
        {'texto': 'Descrição', 'tipo': 'text', 'id': 'descricao', 'nome': 'descricao'},
        {'texto': 'Quantidade', 'tipo': 'number', 'id': 'quantidade', 'nome': 'quantidade'}
    ]
    
    titulo = 'Cadastrar Produto'
    link = '/cadastrar_produto'

    return render_template('cadastro.html', campos=campos, titulo=titulo, link=link)

...

# Função para cadastrar o produto no banco de dados
@app.route('/cadastrar_produto', methods=['POST', 'GET'])
def cadastrar_produto():
    nome = request.form.get('nome')
    marca = request.form.get('marca')
    descricao = request.form.get('descricao')
    quantidade = request.form.get('quantidade')

    conn = mysql.connect()
    cursor = conn.cursor()

    #inserindo no Banco de dados
    cursor.execute("insert into tbl_produtos (nome, marca, descricao, quantidade) VALUES ('%s', '%s', '%s', '%s')"%( nome,marca,descricao,quantidade))
    conn.commit()

    return render_template('confirmacao.html', resposta= nome, titulo="Confirmação")

...

# Função para levar a pagina de busca iniciando com uma lista geral de produtos
@app.route('/listar_produtos', methods=['GET'])
def listar_produtos():
    if session['usuario_logado'] != 'admin':
        return 'Você não tem permissão para acessar essa página. <a href="/">Voltar</a>'
    
    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar e obter os dados dos clientes
    cursor.execute("SELECT * FROM tbl_produtos")
    lista = cursor.fetchall()
    conn.commit()

    nomes = ['Cód', 'Nome', 'Marca', 'Descrição', 'Quantidade']
    editar_btn = '/dados_produtos'
    excluir_btn = '/excluir_produto'
    link = '/buscar_produto'
    busca = 'nome do produto'
    titulo = 'Lista de Produtos'

    return render_template('listar.html', nomes=nomes, titulo=titulo, objetos = lista, editar_btn=editar_btn, excluir_btn=excluir_btn, link=link, busca=busca)

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

    campos = [
        {'id': 'cod', 'nome': 'Cod', 'indice': 0},
        {'id': 'nome', 'nome': 'Nome', 'indice': 1},
        {'id': 'marca', 'nome': 'Marca', 'indice': 2},
        {'id': 'descricao', 'nome': 'Descricao', 'indice': 3},
        {'id': 'quantidade', 'nome': 'Quantidade', 'indice': 4},
    ]
    titulo = 'Editar Produto'
    link = '/editar_produto'

    return render_template('editar.html', objeto = prod, campos=campos, titulo=titulo, link=link)

...

# Função para editar os dados do produto no banco de dados
@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    id = request.form.get('cod')
    nome = str(request.form.get('nome'))
    marca = str(request.form.get('marca'))
    descricao = str(request.form.get('descricao'))
    quantidade = request.form.get('quantidade')
    conn = mysql.connect()
    cursor = conn.cursor()

    #editando o produto no Banco de dados 
    cursor.execute('UPDATE tbl_produtos SET nome = %s, marca = %s, descricao = %s, quantidade = %s  WHERE produto_id = %s',(nome,marca,descricao,quantidade,id))
    conn.commit()
    resposta = "Produto editado com sucesso!"
    return render_template('confirmacao.html', resposta=resposta, titulo="Confirmação")

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

    return render_template('confirmacao.html', resposta= resposta, titulo="Confirmação") 

...

@app.route('/buscar_produto', methods=['POST'])
def buscar_produto():
    nome = request.form.get("busca")
    conn = mysql.connect()
    cursor = conn.cursor()

    #Consulta na tabela de Produtos
    cursor.execute("SELECT * FROM tbl_produtos WHERE nome = %s",(nome))
    lista = cursor.fetchall()
    conn.commit()

    nomes = ['Cód', 'Nome', 'Marca', 'Descrição', 'Quantidade']
    editar_btn = '/dados_produtos'
    excluir_btn = '/excluir_produto'
    link = '/buscar_produto'
    busca = 'nome do produto'
    titulo = 'Buscar Produto'

    return render_template('listar.html', nomes=nomes, titulo=titulo, objetos = lista, editar_btn=editar_btn, excluir_btn=excluir_btn, link=link, busca=busca)
