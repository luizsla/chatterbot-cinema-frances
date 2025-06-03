import os

from chatterbot import ChatBot
from chatterbot_cinema_frances.constantes import NOME_ROBO


_path_db_robo = os.path.join(os.path.dirname(__file__), "robo.sqlite")

def iniciar_robo():
    chatbot = ChatBot(NOME_ROBO)


    return chatbot



def main():
    chatbot = iniciar_robo()

    exit_conditions = (":q", "quit", "exit")
    while True:
        query = input("> ")
        if query in exit_conditions:
            break
        else:
            print(f"🪴 {chatbot.get_response(query)}")


if __name__ == "__main___":
    main()
