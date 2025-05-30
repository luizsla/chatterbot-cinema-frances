from flask import Flask, render_template

from chatterbot_cinema_frances.constantes import PORTA_INTERFACE_CHAT

app = Flask(__name__)

@app.route("/")
def mostrar_interface_chat():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=PORTA_INTERFACE_CHAT)