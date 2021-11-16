import re
from flask import Flask, render_template, request, redirect, session, url_for
from flask.helpers import flash


app = Flask(__name__)
app.secret_key = 'caelum'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usuario1 = Usuario('luan', 'Lua Marques', '1234')
usuario2 = Usuario('nico', 'Nico Steppat', '7a1')
usuario3 = Usuario('flavio', 'Flávio', 'javascript')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3
            }


jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemin Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')

lista = [jogo1, jogo2, jogo3]


@app.route('/')
def index():
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

    lista.append(jogo)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/logout')
def logout():
    usuario = session.pop('usuario_logado', None)
    if usuario:
        flash(f'{usuarios[usuario].nome} deslogado com sucesso!')
    else:
        flash('Nenhum usuario logado!')
    return redirect(url_for('index'))


@app.route('/autenticar', methods=['POST',])
def autenticar():

    usuario_form = request.form['usuario']
    if  usuario_form in usuarios:
        usuario = usuarios[usuario_form]
        if  usuario.senha == request.form['senha']:
            proxima_pagina=request.form['proxima']
            session['usuario_logado']=usuario.id
            flash(f'{usuario.nome}  logou com sucesso!')
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

app.run(threaded=True, debug=True)

