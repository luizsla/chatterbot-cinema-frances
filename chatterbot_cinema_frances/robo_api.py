from flask import Flask

from chatterbot_cinema_frances.constantes import PORTA_INTERFACE_ROBO

app = Flask(__name__)


def _iniciar_robo():
    pass



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



if __name__ == "__main__":
    _iniciar_robo()
    app.run(
        host="127.0.0.1",
        debug=True,
        port=PORTA_INTERFACE_ROBO
    )