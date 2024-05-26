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

@app.route('/agendar_sessao')
def agendar_sessao():
    validacao = False

    return render_template('agendamento.html', validacao=validacao)

@app.route('/pega_data', methods=['GET', 'POST'])
def pega_data():
    dia = request.form.get('data')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    valido = cursor.execute("SELECT * FROM tbl_agenda WHERE dia = %s", (dia,))
    
    if valido > 0:
        cursor.execute("SELECT * FROM tbl_agenda WHERE dia = %s", (dia,))
        horarios = cursor.fetchall()
        cursor.execute("SELECT * FROM tbl_horas")
        horas = cursor.fetchall()
        conn.commit()
        agenda = []
        validacao = True
        for horario in horarios:
            for hora in horas:
                if horario[2] != hora[0]:
                    agenda.append(hora[0])
                else:
                    continue
        return render_template('agendamento.html', agenda=agenda, validacao=validacao)

    else:
        cursor.execute("SELECT * FROM tbl_horas")
        horas = cursor.fetchall()
        agenda = []
        for hora in horas:
            agenda.append(hora[0])
        conn.commit()
        validacao = True
        return render_template('agendamento.html',agenda=agenda, validacao=validacao)


...

@app.route('/agendado', methods=['GET', 'POST'])
def agendado():
    date = request.form['date']
    time = request.form['time']

    conteudo = f'Data: {date}, Hora: {time}'

    return render_template('confirmacao.html', resposta=conteudo, titulo="Confirmação")