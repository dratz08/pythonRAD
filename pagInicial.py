import json

from flask import Flask, render_template, redirect, url_for, request, jsonify
from mysql.connector import Error

import banco
from banco import login_banco, carregamento_home

app = Flask(__name__)

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
            funcionarios = carregamento_home()
            return render_template('home.html', infos=funcionarios)
        else:
            return render_template("login.html", status=res_login)
    else:
        return render_template("login.html", status="Método não permitido")


@app.route("/usuarios/<nome_user>,<celular>")
def usuarios(nome_user, celular):
    return render_template("usuarios.html", nome_user=nome_user, celular=celular)


if __name__ == "__main__":
    app.run(debug=True)
