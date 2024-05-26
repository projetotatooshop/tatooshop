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

@app.route('/menu')
def index():
    return render_template('index.html', titulo="Menu")

...

# Função para levar a pagina de cadastro
@app.route('/cliente_cadastro')
def cliente_cadastro():
    campos = [
        {'texto': 'Nome', 'tipo': 'text', 'id': 'nome', 'nome': 'nome'},
        {'texto': 'E-mail', 'tipo': 'email', 'id': 'email', 'nome': 'email'},
        {'texto': 'Endereço', 'tipo': 'text', 'id': 'endereco', 'nome': 'endereco'},
        {'texto': 'Telefone', 'tipo': 'text', 'id': 'telefone', 'nome': 'telefone'},
        {'texto': 'Idade', 'tipo': 'number', 'id': 'idade', 'nome': 'idade'},
    ]
    titulo = 'Cadastrar Cliente'
    link = '/cadastrar_cliente'
    return render_template('cadastro.html', campos=campos, titulo=titulo, link=link)

...

# Função para cadastrar o cliente no banco de dados
@app.route('/cadastrar_cliente', methods=['POST', 'GET'])
def cadastrar_cliente():
    nome = request.form.get('nome')
    mail = request.form.get('email')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    idade = request.form.get('idade')

    conn = mysql.connect()
    cursor = conn.cursor()
    #buscando email e telefone para verificação
    valida_email = cursor.execute ('select * from tbl_cliente where email =%s', (mail)) 
    valida_telefone = cursor.execute ('select * from tbl_cliente where telefone =%s', (telefone))
     
    #verificando email e telefone
    if valida_email > 0 or valida_telefone > 0:
        resposta = "Usuário já existente!"
        return render_template('confirmacao.html', resposta=resposta, titulo="Confirmação")   
        
    else:
        #inserindo no Banco de dados
        cursor.execute("insert into tbl_cliente (nome, idade, email, endereco, telefone) VALUES ('%s', '%s', '%s', '%s', '%s')"%(nome,idade,mail,endereco,telefone))
        conn.commit()
        return render_template('confirmacao.html', resposta=nome, titulo="Confirmação")

...

# Função para levar a pagina de busca iniciando com uma lista geral de clientes
@app.route('/listar_clientes', methods=['GET'])
def listar_cliente():
    if session['usuario_logado'] != 'admin':
        return 'Você não tem permissão para acessar essa página. <a href="/">Voltar</a>'
    
    conn = mysql.connect()
    cursor = conn.cursor()
    # Consultar e obter os dados dos clientes
    cursor.execute("SELECT usuario_id,nome,idade,email,endereco,telefone FROM tbl_cliente")
    lista = cursor.fetchall()
    conn.commit()
    
    nomes = ['Cód', 'Nome', 'Idade', 'E-mail', 'Endereço', 'Telefone']
    editar_btn = '/dados_cliente'
    excluir_btn = '/excluir_cliente'
    link = '/buscar_cliente'
    busca = 'telefone do cliente'
    titulo = 'Lista de Clientes'

    return render_template('listar.html', nomes=nomes, titulo=titulo, objetos = lista, editar_btn=editar_btn, excluir_btn=excluir_btn, link=link, busca=busca)

...

# Função para levar a pagina de edição do cadastro do cliente no banco de dados
@app.route('/dados_cliente', methods=['POST'])  
def dados_cliente():
    codigo = request.form.get('cod')
    conn = mysql.connect()
    cursor = conn.cursor()  
    # Buscar o registro da pessoa na tabela pelo telefone
    cursor.execute ("SELECT * FROM tbl_cliente WHERE usuario_id=%s",(codigo))   
    cli = cursor.fetchone()
    conn.commit()

    campos = [
        {'id': 'cod', 'nome': 'Cod', 'indice': 0},
        {'id': 'nome', 'nome': 'Nome', 'indice': 1},
        {'id': 'idade', 'nome': 'Idade', 'indice': 2},
        {'id': 'email', 'nome': 'E-mail', 'indice': 4},
        {'id': 'endereco', 'nome': 'Endereço', 'indice': 5},
        {'id': 'telefone', 'nome': 'Telefone', 'indice': 6}
    ]
    titulo = 'Editar Cliente'
    link = '/editar_cliente'

    return render_template('editar.html', objeto = cli, campos=campos, titulo=titulo, link=link)

...

# Função para editar o cadastro do cliente no banco de dados
@app.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    id = request.form.get('cod')
    nome = request.form.get('nome')
    mail = request.form.get('email')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    idade = request.form.get('idade')
    conn = mysql.connect()
    cursor = conn.cursor()

    #buscando email e telefone para verificação
    valida_email = cursor.execute ('select * from tbl_cliente where email =%s AND usuario_id != %s', (mail, id)) 
    valida_telefone = cursor.execute ('select * from tbl_cliente where telefone =%s AND usuario_id != %s', (telefone, id))       

    #verificando email e telefone
    if valida_email > 0 or valida_telefone > 0:
        resposta = "Usuário já existente!"
        return render_template('confirmacao.html', resposta= resposta, titulo="Confirmação")
    else:
        #editando o cliente no Banco de dados 
        cursor.execute('UPDATE tbl_cliente SET nome = %s, idade = %s, email = %s, endereco = %s, telefone = %s  WHERE usuario_id = %s',(nome, idade, mail, endereco, telefone, id))
        conn.commit()
        resposta = "Cliente editado com sucesso!"
        return render_template('confirmacao.html', resposta=resposta, titulo="Confirmação")

...

# Função para excluir o cadastro do cliente no banco de dados
@app.route('/excluir_cliente', methods=['POST'])
def excluir_cliente():
    telefone = str(request.form.get('telefone'))
    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar e obter os dados dos clientes
    if telefone != None:
        cursor.execute('DELETE FROM tbl_cliente WHERE telefone = %s',(telefone))
        conn.commit()
        resposta = "Cliente excluido"

        return render_template('confirmacao.html', resposta= resposta, titulo="Confirmação")
    else:
        resposta = "Cliente não encontrado"
        return render_template('confirmacao.html', resposta= resposta, titulo="Confirmação")

...

@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    telefone = str(request.form.get("busca"))
    conn = mysql.connect()
    cursor = conn.cursor()
    #Consulta na tabela de Clientes
    cursor.execute("SELECT usuario_id,nome,email,endereco,telefone FROM tbl_cliente WHERE telefone=%s",(telefone))

    lista = cursor.fetchall()
    conn.commit()

    nomes = ['Cód', 'Nome', 'Idade', 'E-mail', 'Endereço', 'Telefone']
    editar_btn = '/dados_cliente'
    excluir_btn = '/excluir_cliente'
    link = '/buscar_cliente'
    busca = 'telefone do cliente'
    titulo = 'Buscar Cliente'

    return render_template('listar.html', nomes=nomes, titulo=titulo, objetos = lista, editar_btn=editar_btn, excluir_btn=excluir_btn, link=link, busca=busca)

...

@app.route('/agendamento')
def agendamento_cliente():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_agendamento")
    horarios = cursor.fetchall()
    conn.commit()

    return render_template('agendamento.html', opcoes=horarios)

...

@app.route('/agendado', methods=['GET', 'POST'])
def agendamento():
    date = request.form['date']
    time = request.form['time']

    conteudo = f'Data: {date}, Hora: {time}'

    return render_template('confirmacao.html', resposta=conteudo, titulo="Confirmação")