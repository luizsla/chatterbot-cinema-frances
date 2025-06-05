from chatterbot.trainers import ListTrainer

from chatterbot_cinema_frances.robo import iniciar_robo 


def main():
    chatbot = iniciar_robo()
    treinador = ListTrainer(chatbot)

    print("O treinador é", treinador, id(treinador))

    



if __name__ == "__main__":
    main()