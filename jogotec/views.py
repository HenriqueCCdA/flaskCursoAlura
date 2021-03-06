from time import time

from flask import render_template, request, redirect, session, url_for, send_from_directory
from flask.helpers import flash

from models import Jogo
from dao import JogoDao, UsuarioDao
from helpers import recupera_imagem, remove
from jogoteca import db, app

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
    jogo = jogo_dao.salvar(jogo)
    timestamp = time()
    arquivo = request.files['arquivo']
    path = app.config['UPLOAD_PATH'] / f'capa_{jogo.id}-{timestamp}.jpg'
    arquivo.save(path)
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session:
        return redirect(url_for("login", proxima=url_for('editar', id=id)))

    jogo = jogo_dao.busca_por_id(id)

    nome_arquivo = recupera_imagem(id)
    return render_template('editar.html', jogo=jogo, titulo='Editando o Jogo',
                            capa_jogo=nome_arquivo)

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo = jogo_dao.busca_por_id(id)
    flash(f'O jogo {jogo.nome} foi deletado com sucesso!')
    jogo_dao.deletar(id)
    return redirect(url_for('index'))


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']

    jogo = Jogo(nome, categoria, console, id=id)

    jogo_dao.salvar(jogo)

    timestamp = time()

    arquivo = request.files['arquivo']
    path = app.config['UPLOAD_PATH'] / f'capa_{jogo.id}-{timestamp}.jpg'

    deleta_arquivo(jogo.id)
    arquivo.save(path)

    return redirect(url_for('index'))

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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)