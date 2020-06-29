from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key ="alura"
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo("Super mario","Ação","SNES")
jogo2 = Jogo("Pokemon Gold","RPG","Game Boy")
jogo3 = Jogo("Mortal Kombat", "RPG", "SNES")
lista =[jogo1, jogo2, jogo3]
@app.route('/')
def index():
    return render_template('lista.html',titulo="jogos", jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html',titulo="Novo Jogo")

@app.route('/criar',methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar',methods=['POST'])
def autenticar():
    if 'mestra' in request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + ', Você agora esta logado!')
        return redirect('/')
    else:
        flash("Falha na senha ou no usuário")
        return redirect('/login')
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return  redirect('/')
    
app.run(debug=True)
