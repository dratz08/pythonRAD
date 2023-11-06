from flask import Flask, render_template, request, session, url_for

from banco import login_banco, carregamento_home, dados_edicao, update_edicao, logar_horas, del_user, add_user

app = Flask(__name__)
app.secret_key = 'asdklasdiw30u1w0e9qwmasda'

# route/Function
@app.route("/")
def homepage():
    return render_template("login.html", status="")


@app.route("/home", methods=['POST'])
def home():
    if request.method == 'POST':
        # Atualização da tela home após update de usuário
        if request.form.get(key='id_edit'):
            id_edit = request.form['id_edit']
            nome_edit = request.form['nome_edit']
            salario_edit = request.form['salario_edit']
            endereco_edit = request.form['endereco_edit']
            cargo_edit = request.form['cargo_edit']
            adm_edit = request.form['adm_edit']
            update_edicao(id_edit, nome_edit, salario_edit, endereco_edit, cargo_edit, adm_edit)
            consulta = carregamento_home(session['username'])
            num_projetos = len(consulta[3])
            return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0], projetos=consulta[3], num_proj=num_projetos)
        # Atualização da tela home após adição de usuário
        elif request.form.get(key='nome_add'):
            nome_add = request.form['nome_add']
            senha_add = request.form['senha_add']
            salario_add = request.form['salario_add']
            endereco_add = request.form['endereco_add']
            cargo_add = request.form['cargo_add']
            adm_add = request.form['adm_add']
            add_user(nome_add, senha_add, salario_add, endereco_add, cargo_add, adm_add)
            consulta = carregamento_home(session['username'])
            num_projetos = len(consulta[3])
            return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0],
                                   projetos=consulta[3], num_proj=num_projetos)
        else:
            return render_template("home.html")
    return render_template("home.html")


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        psswrd = request.form['password']
        res_login = login_banco(user, psswrd)
        if res_login == "Credenciais corretas":
            session['username'] = user
            consulta = carregamento_home(user)
            num_projetos = len(consulta[3])
            return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0], projetos=consulta[3], num_proj=num_projetos)
        else:
            return render_template("login.html", status=res_login)
    else:
        return render_template("login.html", status="Método não permitido")


@app.route("/edit", methods=['POST'])
def edit():
    if request.method == 'POST':
        id_user = request.form['id']
        dados = dados_edicao(id_user)
        return render_template("edit.html", dados=dados[0])


@app.route("/log_horas", methods=['POST'])
def log_horas():
    if request.method == 'POST':
        horas = list(request.form.to_dict().values())
        projeto = list(request.form.to_dict().keys())
        logar_horas(projeto[0], horas[0], session['username'])
        consulta = carregamento_home(session['username'])
        num_projetos = len(consulta[3])
        return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0], projetos=consulta[3], num_proj=num_projetos)

@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':
        id_delete = request.form['id']
        del_user(id_delete)
        consulta = carregamento_home(session['username'])
        num_projetos = len(consulta[3])
        return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0], projetos=consulta[3], num_proj=num_projetos)

@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
