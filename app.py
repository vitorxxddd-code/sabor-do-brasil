import json
import os
from flask import Flask, render_template, request, jsonify, session 
from controllers import usuario_controller, receita_controller 
from utils.persistencia import ler_dados 

app = Flask(__name__) 
app.secret_key = "chave_mestra_2024" 

@app.route("/") 
def index():
    dados = ler_dados() 
    return render_template(
        "index.html",
        receitas=dados.get("receitas", []),
        usuario=session.get("usuario")
    )

@app.route("/cadastrar", methods=["POST"]) 
def cadastrar():
    dados = request.get_json() or {}
    
    res, status = usuario_controller.processar_cadastro(
        dados.get('nickname'),
        dados.get('senha')
    )
    return jsonify(res), status 

@app.route("/login", methods=["POST"]) 
def login():
    dados = request.get_json() or {}

    res, status = usuario_controller.processar_login(
        dados.get('nickname'),
        dados.get('senha')
    )

    # 🔥 salva usuário na sessão se login ok
    if status == 200:
        session["usuario"] = res.get("usuario")

    return jsonify(res), status 

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario", None) 
    return jsonify({"mensagem": "Saiu!"}) 

@app.route("/curtir/<int:receita_id>", methods=["POST"]) 
def curtir(receita_id):  # ✅ corrigido: receber parâmetro
    user = session.get("usuario") 
    if not user: 
        return jsonify({"erro": "Logue primeiro"}), 401 

    res, status = receita_controller.alternar_curtida(
        receita_id, user.get("nickname")
    )
    return jsonify(res), status  # ✅ corrigido retorno

@app.route("/comentario/<int:comentario_id>", methods=["DELETE"])
def remover_comentario(comentario_id):  # ✅ corrigido: receber parâmetro
    user = session.get("usuario") 
    if not user: 
        return jsonify({"erro": "Logue primeiro"}), 401

    res, status = receita_controller.remover_comentario(
        comentario_id, user
    )
    return jsonify(res), status 

if __name__ == "__main__": 
    app.run(debug=True)