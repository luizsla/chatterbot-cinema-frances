from flask import Flask, request

from chatterbot_cinema_frances.constantes import PORTA_INTERFACE_ROBO
from chatterbot_cinema_frances.robo import iniciar_robo

app = Flask(__name__)

_robo_client = iniciar_robo()


@app.route("/responder")
def hello_world():
    try:
        resposta = _robo_client.get_response()
    except KeyError:
        pass



if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        debug=True,
        port=PORTA_INTERFACE_ROBO
    )