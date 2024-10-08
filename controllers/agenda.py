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

@app.route('/agendamento')
def agendamento():
    validacao = False
    telefone = True
    return render_template('agendamento.html', validacao_telefone=telefone, validacao=validacao)

...

@app.route('/busca_agenda')
def busca_agenda():
    busca = False
    return render_template('busca_agenda.html', busca=busca)

...

@app.route('/pega_data', methods=['GET', 'POST'])
def pega_data():
    #recebe data
    dia = request.form.get('data')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    valido = cursor.execute("SELECT * FROM tbl_agenda WHERE dia = %s", (dia,))
    
    #confirma se tem sessao agendada pra esse dia
    if valido > 0:
        sessoes = []
        cursor.execute("SELECT * FROM tbl_agenda WHERE dia = %s", (dia,))
        horarios = cursor.fetchall()
        for sessao in horarios:
            sessoes.append(sessao[2])

        cursor.execute("SELECT * FROM tbl_horas")
        horas = cursor.fetchall()
        conn.commit()
        agenda = []
        validacao = True
        for hora in horas:
            if hora[0] not in sessoes:
                agenda.append(hora[0])
            else:
                pass
        return render_template('agendamento.html', dia=dia, agenda=agenda, validacao=validacao)

    else:
        cursor.execute("SELECT * FROM tbl_horas")
        horas = cursor.fetchall()
        agenda = []
        for hora in horas:
            agenda.append(hora[0])
        conn.commit()
        validacao = True
        return render_template('agendamento.html', dia=dia, agenda=agenda, validacao=validacao)

...

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    data = request.form['dia']
    hora = request.form['time']
    telefone = request.form['telefone']
    pagamento = "A escolher"
    valor = 0
    situacao = "Ok"

    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()

    #buscando telefone para verificação
    valida_telefone = cursor.execute ('select * from tbl_cliente where telefone =%s', (telefone))
    agendado = cursor.execute ('select * from tbl_agenda where dia=%s AND telefone =%s', (data, telefone))
        
    #validando telefone
    if valida_telefone > 0 and agendado == 0:
        #se telefone está cadastrado, prosiga com o agendamento
        cursor.execute("insert into tbl_agenda (dia, horario, telefone, tipo_pagamento, valor_total, situacao) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(data, hora, telefone, pagamento, valor, situacao))
        conn.commit()
        conteudo = "Agendamento realizado com sucesso!"

        return render_template('confirmacao.html', resposta=conteudo, titulo="Confirmação")

    #se o telefone não está cadastrado, não siga com o agendamento
    else:
        val_tel = False
        conteudo = "Erro relacionado ao telefone! Verifique se não há nenhum agendamento para este telefone ou se o telefone está cadastrado."
        return render_template('agendamento.html',resposta=conteudo, validacao_telefone=val_tel)

...

@app.route('/lista_agenda', methods=['GET', 'POST'])
def lista_agenda():
    #recebendo data do formulário
    data = request.form['dia']
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    #buscando agenda
    cursor.execute("SELECT A.agenda_id, C.nome, A.dia, A.horario, A.telefone, A.tipo_pagamento, A.valor_total, A.situacao FROM tbl_agenda AS A INNER JOIN tbl_cliente AS C ON A.telefone = C.telefone where A.dia = %s", (data,))
    agenda = cursor.fetchall()
    conn.commit()
    nomes = ['Cód', 'Nome', 'Dia', 'Hora', 'Telefone', 'Forma de Pagamento', 'Valor Total', 'Situação']
    busca = True
    return render_template('busca_agenda.html',busca=busca, nomes=nomes, lista=agenda)

...

@app.route('/excluir_agenda', methods=['GET', 'POST'])
def excluir_agenda():
    #recebendo informação do formulário
    cod_agenda = request.form['cod']
    #conectando com DB
    conn = mysql.connect()
    cursor = conn.cursor()
    #buscando agenda
    cursor.execute('DELETE FROM tbl_agenda WHERE agenda_id = %s', (cod_agenda,))
    conn.commit()
    conteudo = "Agendamento excluído com sucesso!"
    return render_template('confirmacao.html', resposta=conteudo, titulo="Confirmação")

...

@app.route('/dados_agenda', methods=['POST'])
def dados_agenda():
    codigo = request.form.get('cod')
    conn = mysql.connect()
    cursor = conn.cursor()  
    # Buscar o registro da pessoa na tabela pelo telefone
    cursor.execute ("SELECT * FROM tbl_agenda WHERE agenda_id=%s",(codigo))
    cli = cursor.fetchone()
    conn.commit()

    campos = [
        {'id': 'cod', 'nome': 'Cod', 'indice': 0},
        {'id': 'telefone', 'nome': 'Telefone', 'indice': 1},
        {'id': 'dia', 'nome': 'Dia', 'indice': 2},
        {'id': 'horario', 'nome': 'Horário', 'indice': 3}
        
    ]
    titulo = 'Editar Agendamento'
    link = '/editar_agenda'

    #listar horarios disponiveis
    sessoes = []
    cursor.execute("SELECT * FROM tbl_agenda WHERE dia = %s", (cli[1],))
    horarios = cursor.fetchall()
    for sessao in horarios:
        sessoes.append(sessao[2])
    cursor.execute("SELECT * FROM tbl_horas")
    horas = cursor.fetchall()
    conn.commit()
    agenda = []
    for hora in horas:
        if hora[0] not in sessoes:
            agenda.append(hora[0])
            validacao = False
        else:
            pass

    return render_template('editar_agenda.html', objeto = cli, agenda=agenda, campos=campos, titulo=titulo, link=link, validacao=validacao)

...

@app.route('/editar_agenda', methods=['POST'])
def editar_agenda():
    id = request.form.get('cod')
    dia = request.form.get('dia')
    horario = request.form.get('horario')
    conn = mysql.connect()
    cursor = conn.cursor()

    
    cursor.execute('UPDATE tbl_agenda SET dia = %s, horario = %s WHERE agenda_id = %s',(dia, horario, id))
    conn.commit()
    resposta = "Agendamento editado com sucesso!"
    return render_template('confirmacao.html', resposta=resposta, titulo="Confirmação")

...

@app.route('/pega_data_reagenda', methods=['POST'])
def pega_data_reagenda():
    codigo = request.form.get('cod')
    dia = request.form.get('dia')
    conn = mysql.connect()
    cursor = conn.cursor()  
    # Buscar o registro da pessoa na tabela pelo telefone
    cursor.execute ("SELECT * FROM tbl_agenda WHERE agenda_id=%s",(codigo))
    cli = cursor.fetchone()
    conn.commit()

    campos = [
        {'id': 'cod', 'nome': 'Cod', 'indice': 0},
        {'id': 'telefone', 'nome': 'Telefone', 'indice': 1},
        {'id': 'dia', 'nome': 'Dia', 'indice': 2},
        {'id': 'horario', 'nome': 'Horário', 'indice': 3}
        
    ]
    titulo = 'Editar Agendamento'
    link = '/editar_agenda'

    #listar horarios disponiveis
    sessoes = []
    cursor.execute("SELECT * FROM tbl_agenda WHERE dia = %s", (dia))
    horarios = cursor.fetchall()
    for sessao in horarios:
        sessoes.append(sessao[2])
    cursor.execute("SELECT * FROM tbl_horas")
    horas = cursor.fetchall()
    conn.commit()
    agenda = []
    for hora in horas:
        if hora[0] not in sessoes:
            agenda.append(hora[0])
            validacao = False
        else:
            pass
    cli = list(cli)
    cli[1] = dia
    cli = tuple(cli)
    return render_template('editar_agenda.html', objeto = cli, agenda=agenda, campos=campos, titulo=titulo, link=link, validacao=validacao)