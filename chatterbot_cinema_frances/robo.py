from chatterbot import ChatBot
from chatterbot_cinema_frances.constantes import NOME_ROBO

def iniciar_robo():
    chatbot = ChatBot(NOME_ROBO, database_uri=f"sqlite:///chat.sqlite3")

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


if __name__ == "__main__":
    main()
