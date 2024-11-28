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
    #zerar tbl_temp_cliente
    cursor.execute("DELETE FROM tbl_temp_cliente")
    conn.commit()
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

...

@app.route('/finalizar_compra', methods=['GET', 'POST'])
def finalizar_compra():
    cod = request.form.get('cod')
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    #buscar dados do cliente
    cursor.execute('SELECT * FROM tbl_temp_cliente WHERE id = %s', (cod,))
    cliente = cursor.fetchone()
    conn.commit()
    #busca tudo do carrinho
    cursor.execute("SELECT * FROM tbl_carrinho WHERE id = %s", (cod))
    carrinho = cursor.fetchall()
    conn.commit()
    #apagar dados do carrinho
    #cursor.execute("DELETE FROM tbl_carrinho WHERE id = %s", (cod))
    #conn.commit()
    formas = ['Pix', 'Dinheiro', 'Credito', 'Debito']
    itens = ['Cód Carrinho', 'item', 'quantidade']
    campos = ['Cód', 'Nome', 'Dia', 'Hora', 'Telefone']
    return render_template('pagamento.html', cliente=cliente, carrinho=carrinho, campos=campos, itens=itens, formas=formas)

...

@app.route('/pagar', methods=['GET', 'POST'])
def pagar():
    cod = request.form.get('cod')
    forma = request.form.get('forma')
    valor = request.form.get('valor')
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    #buscar dados do cliente
    cursor.execute('SELECT * FROM tbl_temp_cliente WHERE id = %s', (cod,))
    cliente = cursor.fetchone()
    conn.commit()
    #busca tudo do carrinho
    cursor.execute("SELECT * FROM tbl_carrinho WHERE id = %s", (cod))
    carrinho = cursor.fetchall()
    conn.commit()
    produtos = ', '.join([f'{item[2]}x {item[1]}' for item in carrinho])
    #apagar dados do carrinho
    cursor.execute("DELETE FROM tbl_carrinho")
    conn.commit()
    #registrar na tabela pagamento
    cursor.execute("INSERT INTO tbl_pagamento (nome, dia, horario, telefone, produtos, valor, forma ) VALUES (%s, %s, %s, %s, %s, %s, %s)", (cliente[1], cliente[2], cliente[3], cliente[4], produtos, valor, forma))
    conn.commit()
    cursor.execute('UPDATE tbl_agenda SET situacao = "Finalizado", valor_total = %s, tipo_pagamento = %s WHERE agenda_id = %s', (valor, forma, cod))
    conn.commit()
    #limpa tabela temporaria
    cursor.execute('DELETE FROM tbl_temp_cliente')
    conn.commit()

    resposta = "Pagamento realizado"
    return render_template('confirmacao.html', resposta=resposta)

...

@app.route('/caixa', methods=['GET', 'POST'])
def caixa():
    busca = False
    valido = True
    return render_template('caixa.html', busca=busca, valido=valido)

...

@app.route('/dia_caixa', methods=['GET', 'POST'])
def dia_caixa():
    #recebe data
    dia = request.form.get('dia')
    #verifica se existe algum pagamento no dia
    conn = mysql.connect()
    cursor = conn.cursor()
    valido = cursor.execute("SELECT * FROM tbl_pagamento WHERE dia = %s" , (dia,))
    conn.commit()
    #Caso sim
    if valido > 0:
        #seleciona pagamentos do dia
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_pagamento WHERE dia = %s" , (dia,))
        pagamentos = cursor.fetchall()
        conn.commit()
        #seleciona os valores de cada forma de pagamento
        cursor.execute("SELECT * FROM tbl_pagamento WHERE dia = %s AND forma = 'Pix'" , (dia,))
        pix = cursor.fetchall()
        conn.commit()
        pix = list(pix)
        #soma dos valores em pix
        valor_pix = 0
        for n in pix:
            valor = n[6]
            valor_pix += valor
        #soma dos valores em dinheiro
        cursor.execute("SELECT * FROM tbl_pagamento WHERE dia = %s AND forma = 'Dinheiro'" , (dia,))
        dinheiro = cursor.fetchall()
        dinheiro = list(dinheiro)
        conn.commit()
        valor_dinheiro = 0
        for n in dinheiro:
            valor = n[6]
            valor_dinheiro += valor
        #soma dos valores em credito
        cursor.execute("SELECT * FROM tbl_pagamento WHERE dia = %s AND forma = 'Credito'" , (dia,))
        credito = cursor.fetchall()
        credito = list(credito)
        conn.commit()
        valor_credito = 0
        for n in credito:
            valor = n[6]
            valor_credito += valor
        #soma dos valores em debito
        cursor.execute("SELECT * FROM tbl_pagamento WHERE dia = %s AND forma = 'Debito'" , (dia,))
        debito = cursor.fetchall()
        debido = list(debito)
        conn.commit()
        valor_debito = 0
        for n in debito:
            valor = n[6]
            valor_debito += valor
        #somando todos os valores
        total = valor_pix + valor_dinheiro + valor_credito + valor_debito
        nomes = ['Cód', 'Nome', 'Dia', 'Hora', 'Telefone', 'Produtos', 'Valor Pago', 'Forma de Pagamento']
        busca = True
        valido = True
    #caso não
    else:
        nomes = ['Cód', 'Nome', 'Dia', 'Hora', 'Telefone', 'Produtos', 'Valor Pago', 'Forma de Pagamento']
        pagamentos = []
        valor_dinheiro = 0
        valor_pix = 0
        valor_credito = 0
        valor_debito = 0
        total = 0
        busca = False
        valido = False


    return render_template('caixa.html', valido=valido, busca=busca, total=total, pagamentos=pagamentos, dinheiro=valor_dinheiro , pix=valor_pix, credito=valor_credito, debito=valor_debito, nomes=nomes)

...


