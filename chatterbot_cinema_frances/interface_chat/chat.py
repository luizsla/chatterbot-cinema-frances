import requests
import secrets

from http import HTTPStatus
from flask import Flask, render_template, request, session, send_from_directory

from chatterbot_cinema_frances.constantes import CONFIANCA_MINIMA, PORTA_INTERFACE_CHAT, URL_ROBO_API, MODO_PESQUISA_SINOPSES
from chatterbot_cinema_frances.database import buscar_sinopses_por_tags

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def mostrar_interface_chat():
    return render_template("index.html")


@app.get("/sinopses/<path:nome_arquivo>")
def download_artigo(nome_arquivo):
    return send_from_directory("static/arquivos", nome_arquivo, as_attachment=True)


@app.route("/robo/perguntar/")
def perguntar_robo():
    try:
        if session.get("em_modo_pesquisa", False):
            tags = request.args["pergunta"].split(",")
            sinopses = buscar_sinopses_por_tags(tags)
            session["em_modo_pesquisa"] = False

            return {"sinopses": sinopses, "modo": "pesquisa"}
        
        resposta = requests.post(f"{URL_ROBO_API}/responder", json={"pergunta": request.args["pergunta"]})
        assert resposta.status_code == HTTPStatus.OK, 'Erro na comunicação entre chatAPI e roboAPI'
        dados_resposta = resposta.json()

        if dados_resposta["confianca"] < CONFIANCA_MINIMA:
            raise ValueError("Resposta não alcançou confiança mínima de %.2f. Por favor, tente novamente com outro texto." % CONFIANCA_MINIMA)
        
        session["em_modo_pesquisa"] = True if  request.args["pergunta"] == MODO_PESQUISA_SINOPSES else False

        return {"resposta": dados_resposta["resposta"], "confianca": dados_resposta["confianca"], "modo": "chat"}
    except KeyError:
        return {"erro": "Parâmetro `GET` *pergunta* obrigatório"}, HTTPStatus.BAD_REQUEST
    except AssertionError as exp:
        return {"erro": str(exp)}, HTTPStatus.INTERNAL_SERVER_ERROR
    except ValueError as exp:
        return {"erro": str(exp)}, HTTPStatus.BAD_REQUEST



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=PORTA_INTERFACE_CHAT)