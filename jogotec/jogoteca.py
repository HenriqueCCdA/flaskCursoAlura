import re
from flask import Flask, render_template, request, redirect, session, url_for
from flask.helpers import flash
from flask_mysqldb import MySQL

from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao


app = Flask(__name__)
app.secret_key = 'alura'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alura'
app.config['MYSQL_DB'] = 'jogoteca'
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos = lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session:
        return redirect(url_for("login", proxima=url_for('novo')))
    return render_template('novo.html', titulo = 'Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)

    jogo_dao.salvar(jogo)

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session:
        return redirect(url_for("login", proxima=url_for('editar')))

    jogo = jogo_dao.busca_por_id(id)

    return render_template('editar.html', jogo=jogo, titulo='Editando o Jogo')

@app.route('/atualizar', methods=['POST',])
def atualizar():
    pass

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/logout')
def logout():
    usuario = usuario_dao.busca_por_id(session.pop('usuario_logado', None))
    if usuario:
        flash(f'{usuario.nome} deslogado com sucesso!')
    else:
        flash('Nenhum usuario logado!')
    return redirect(url_for('index'))


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])

    if usuario:
        if  usuario.senha == request.form['senha']:
            session['usuario_logado']=usuario.id
            flash(f'{usuario.nome}  logou com sucesso!')
            proxima_pagina=request.form['proxima']
            return redirect(proxima_pagina)

    flash('Senha e/ou usuarios incorretos, tente novamente!')
    return redirect(url_for('login'))

app.run(threaded=True, debug=True)
