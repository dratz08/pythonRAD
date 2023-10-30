from flask import Flask, render_template, request, session

from banco import login_banco, carregamento_home, dados_edicao, update_edicao

app = Flask(__name__)
app.secret_key = 'asdklasdiw30u1w0e9qwmasda'

# route/Function
@app.route("/")
def homepage():
    return render_template("login.html", status="")


@app.route("/home")
def home():
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
            return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0])
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

@app.route("/home_editada", methods=['POST'])
def home_editada():
    if request.method == 'POST':
        id_edit = request.form['id']
        nome_edit = request.form['nome']
        salario_edit = request.form['salario']
        endereco_edit = request.form['endereco']
        cargo_edit = request.form['cargo']
        adm_edit = request.form['adm']
        #print([id_edit, nome_edit, salario_edit, endereco_edit, cargo_edit, adm_edit])
        update_edicao(id_edit, nome_edit, salario_edit, endereco_edit, cargo_edit, adm_edit)
        consulta = carregamento_home(session['username'])
        return render_template('home.html', infos_func=consulta[0], infos_prod=consulta[1], adm=consulta[2][0][0])


if __name__ == "__main__":
    app.run(debug=True)
