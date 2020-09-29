from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from mysql import connector
import pymysql, os, time

from models import Jogo, Usuario

db = connector.connect()
app = Flask(__name__)
app.secret_key = "alura"

host = '0.0.0.0'
user = 'admin'
password = '39411434'
port = 3306
db = 'jogoteca'
# dirname = nome do diretório... aspath = pega o nome do caminho abosluto em relação ao arquivo atual(jogoteca)
root_path = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

db = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db)

jogo_dao = JogoDao(db)

app.config['feijao'] = "branquinho"
feijao = app.config['feijao']
print("legumes", feijao)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo="jogos", jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo="Novo Jogo")


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']
    timestamp = time.time()
    arquivo.save(f'{root_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo="Editando Jogo", jogo=jogo, capa_jogo=nome_imagem or 'capa_padrao.jpg')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(root_path):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

def deleta_arquivo():
    arquivo = recupera_imagem(id)
    os.remove(os.path.join(root_path, arquivo))


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    arquivo = request.files['arquivo']
    upload_path = root_path
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ', Você agora esta logado!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash("Falha na senha ou no usuário")
            return redirect(url_for('login'))

    else:
        flash("Falha na senha ou no usuário")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return redirect(url_for('index'))  # redireciona para a rota index


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O Jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


app.run(debug=True)
