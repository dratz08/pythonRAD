import mysql.connector
from mysql.connector import Error


def ConexaoBDAcademico():  # conexão com o BD
    con = None
    try:
        con = mysql.connector.connect(host='pythonrad.mysql.uhserver.com', user='dratovsky', password='dratz@217122185',
                                      database='pythonrad'
                                      )
    except Error as ex:
        print(ex)
    return con

def login_banco(usuario, senha):  # select
    vcon = ConexaoBDAcademico()
    cursor = vcon.cursor()
    query = f"SELECT id FROM usuarios WHERE usuario = '{usuario}'"
    cursor.execute(query)
    resposta1 = cursor.fetchall()
    if not resposta1:
        vcon.close()
        return "Usuário Inexistente"
    else:
        query_senha = f"SELECT senha FROM usuarios WHERE id = '{resposta1[0][0]}'"
        cursor.execute(query_senha)
        resposta2 = cursor.fetchall()
        if resposta2[0][0] == senha:
            vcon.close()
            return "Credenciais corretas"
        else:
            vcon.close()
            return "Senha Incorreta"


def carregamento_home():
    try:
        vcon = ConexaoBDAcademico()
        cursor = vcon.cursor()
        cursor.execute(f"SELECT * FROM funcionarios")
        infos_funcionarios = cursor.fetchall()
        resposta = []
        infos = []
        for info in infos_funcionarios:
            infos.append(info)

        cursor.execute(f"SELECT  `funcionarios`.`nome`, `carga horaria projetos`.`Python RAD`, "
                       f"`carga horaria projetos`.`Comercio C&A`, `carga horaria projetos`.`Banco do Brasil` FROM "
                       f"`carga horaria projetos`, `funcionarios` WHERE `carga horaria projetos`.`id` =  "
                       f"`funcionarios`.`id`")
        prod = cursor.fetchall()
        info_prod = []
        for info in prod:
            info_prod.append(info)
        vcon.close()
        resposta.append(infos)
        print(info_prod)
        resposta.append(info_prod)
        return resposta
    except Error as ex:
        print(ex)