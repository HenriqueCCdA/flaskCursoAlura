from os import listdir, remove
from jogoteca import app


def recupera_imagem(id):
    for nome_arquivo in listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo:
        path = app.config['UPLOAD_PATH'] / arquivo
        remove(path)