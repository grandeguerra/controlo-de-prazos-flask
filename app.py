from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Troca isto por algo seguro em produção

DADOS_PATH = os.path.join(os.path.dirname(__file__), "dados")
PROCESSOS_PATH = os.path.join(DADOS_PATH, "processos.json")

# Função para carregar processos
def ler_processos_json():
    if not os.path.exists(PROCESSOS_PATH):
        return {}
    with open(PROCESSOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para guardar processos
def gravar_processos_json(processos):
    with open(PROCESSOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(processos, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    processos = ler_processos_json()
    return render_template("index.html", processos=processos)

@app.route("/novo_processo", methods=["GET", "POST"])
def novo_processo():
    if request.method == "POST":
        numero = request.form["numero"]
        cliente = request.form["cliente"]
        comarca = request.form["comarca"]
        data_registo = request.form["data_registo"]
        # Lê atuais
        processos = ler_processos_json()
        if numero in processos:
            flash("Já existe um processo com esse número!")
            return redirect(url_for("novo_processo"))
        processos[numero] = {
            "numero_processo": numero,
            "nome_cliente": cliente,
            "comarca": comarca,
            "data_registo": data_registo,
            "eventos": [],
        }
        gravar_processos_json(processos)
        flash("Processo criado com sucesso!")
        return redirect(url_for("index"))
    return render_template("novo_processo.html")

# Adiciona rotas para editar, eliminar, ver detalhes, etc.

if __name__ == "__main__":
    app.run(debug=True)
