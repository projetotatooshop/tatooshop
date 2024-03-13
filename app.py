import os
from flask import Flask, render_template, json, request
from pprint import pprint
import mysql.connector as mc

app = Flask(__name__)

#conexao com DB
mysql = mc.connect(host = 'localhost', user = 'root', password = 'senha123', database = 'tatto_shop')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
    pprint(request.form)
    nome = request.form.get('nome')
    mail = request.form.get('email')
    tel = request.form.get('fone')
    endereco = request.form.get('end')
    idade = request.form.get('idade')

    #conn = mysql.connection
    cursor = mysql.cursor()
    cursor.execute("insert into tbl_cliente (nome, idade, email, endereco, telefone) VALUES ('%s', '%s', '%s', '%s', '%s')"%( nome,idade,mail,endereco,tel))
    mysql.commit()

    #cursor.execute("SELECT * FROM tbl_cliente WHERE nome = (nome)" %(nome))




    return render_template('confirmacao.html', user= nome)






if __name__ == '__main__':
    app.run(debug=True)