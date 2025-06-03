import os
import requests

from http import HTTPStatus
from flask import Flask, render_template, request, jsonify

from chatterbot_cinema_frances.constantes import PORTA_INTERFACE_CHAT

app = Flask(__name__)

@app.route("/")
def mostrar_interface_chat():
    return render_template("index.html")



@app.route("/robo/perguntar/")
def perguntar_robo():
    try:
        resposta = requests.post({"pergunta": request.args["pergunta"]})
        assert resposta.status_code == HTTPStatus.OK, 'Erro na comunicação entre chatAPI e roboAPI'
        dados_resposta = resposta.json()

        return {"resposta": dados_resposta["resposta"]}
    except KeyError:
        return jsonify(data={"erro": "Parâmetro `GET` *pergunta* obrigatório"}), HTTPStatus.BAD_REQUEST
    except AssertionError as exp:
        return jsonify(data={"erro": str(exp)}), HTTPStatus.INTERNAL_SERVER_ERROR



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=PORTA_INTERFACE_CHAT)