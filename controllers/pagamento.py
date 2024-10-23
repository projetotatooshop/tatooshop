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


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    cod = request.form.get('cod_cliente')
    nome = request.form.get('nome_cliente')
    dia = request.form.get('dia_cliente')
    hora = request.form.get('hora_cliente')
    tel = request.form.get('tel_cliente')
    
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    #manter informacoes do cliente e agenda usando banco de dados
    cursor.execute("INSERT INTO tbl_temp_cliente (id, nome, dia, horario, telefone) VALUES (%s, %s, %s, %s, %s)", (cod, nome, dia, hora, tel))
    conn.commit()
    cliente = (cod, nome, dia, hora, tel)

    # Consultar e obter os dados dos produtos
    cursor.execute("SELECT * FROM tbl_produtos WHERE quantidade > 0")
    produtos = cursor.fetchall()
    produtos = list(produtos)
    conn.commit()
    campos = ['Cód', 'Nome', 'Dia', 'Hora', 'Telefone']
    titulo = 'Carrinho de produtos'
    #link = '/editar_agenda'
    valido = False
    return render_template('carrinho.html', titulo=titulo, campos=campos, cliente=cliente,  produtos=produtos, valido=valido)

...

@app.route('/add_carrinho', methods=['GET', 'POST'])
def add_carrinho():
    #buscar informacoes do cliente e agenda
    cod = request.form.get('cod')
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tbl_temp_cliente WHERE id = %s', (cod,))
    cliente = cursor.fetchone()
    conn.commit()
    #adicionar produtos
    item = request.form.get('item')
    quantidade = request.form.get('quantidade')
    conn = mysql.connect()
    cursor = conn.cursor()
    #adcionar itens no carrinho
    cursor.execute("INSERT INTO tbl_carrinho (id, item, quantidade) VALUES (%s, %s, %s)", (cod, item, quantidade))
    conn.commit()

    carrinho = cursor.execute("SELECT * FROM tbl_carrinho WHERE id = %s", (cod))
    carrinho = cursor.fetchall()
    conn.commit()
    # Consultar e obter os dados dos produtos
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_produtos WHERE quantidade > 0")
    produtos = cursor.fetchall()
    produtos = list(produtos)
    conn.commit()  
    campos = ['Cód', 'Nome', 'Dia', 'Hora', 'Telefone']

    #manter titulo
    titulo = 'Carrinho de produtos'
    valido = True
    return render_template('carrinho.html', titulo=titulo, campos=campos, cliente=cliente,  produtos=produtos, carrinho=carrinho, valido=valido)