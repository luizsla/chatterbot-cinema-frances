import requests

from http import HTTPStatus
from flask import Flask, render_template, request

from chatterbot_cinema_frances.constantes import CONFIANCA_MINIMA, PORTA_INTERFACE_CHAT, URL_ROBO_API

app = Flask(__name__)

@app.route("/")
def mostrar_interface_chat():
    return render_template("index.html")



@app.route("/robo/perguntar/")
def perguntar_robo():
    try:
        resposta = requests.post(f"{URL_ROBO_API}/responder", json={"pergunta": request.args["pergunta"]})
        assert resposta.status_code == HTTPStatus.OK, 'Erro na comunicação entre chatAPI e roboAPI'
        dados_resposta = resposta.json()

        if dados_resposta["confianca"] < CONFIANCA_MINIMA:
            raise ValueError("Resposta não alcançou confiança mínima de %.2f. Por favor, tente novamente com outro texto." % CONFIANCA_MINIMA)

        return {"resposta": dados_resposta["resposta"]}
    except KeyError:
        return {"erro": "Parâmetro `GET` *pergunta* obrigatório"}, HTTPStatus.BAD_REQUEST
    except AssertionError as exp:
        return {"erro": str(exp)}, HTTPStatus.INTERNAL_SERVER_ERROR
    except ValueError as exp:
        return {"erro": str(exp)}, HTTPStatus.BAD_REQUEST



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=PORTA_INTERFACE_CHAT)