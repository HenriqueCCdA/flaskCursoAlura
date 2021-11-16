import re
from flask import Flask, render_template, request, redirect, session
from flask.helpers import flash


app = Flask(__name__)
app.secret_key = 'caelum'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


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
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo = 'Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)

    lista.append(jogo)

    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/logout')
def logout():
    usuario = session.pop('usuario_logado', None)
    if usuario:
        flash(f'{usuario} deslogado com sucesso!')
    else:
        flash('Nenhum usuario logado!')
    return redirect('/login')


@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'mestra' == request.form['senha']:
        usuario=request.form['usuario']
        proxima_pagina=request.form['proxima']
        session['usuario_logado']=usuario
        flash(f'{usuario}  logou com sucesso!')
        return redirect(f'/{proxima_pagina}')
    else:
        flash('Não logado, tente novamente!')
        return redirect('/login')

app.run(debug=True)

