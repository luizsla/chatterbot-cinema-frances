from http import HTTPStatus

from flask import Flask, render_template, request, Response, jsonify

from chatterbot_cinema_frances.constantes import PORTA_INTERFACE_CHAT

app = Flask(__name__)

@app.route("/")
def mostrar_interface_chat():
    return render_template("index.html")



@app.route("/robo/perguntar/")
def perguntar_robo():
    try:
        pergunta = request.args["pergunta"]
        print("Irei perguntar o robô aqui!")
        
        return {"resposta": pergunta}
    except KeyError:
        return jsonify(data={"erro": "Parâmetro `GET` *pergunta* obrigatório"}), HTTPStatus.BAD_REQUEST



if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=PORTA_INTERFACE_CHAT)