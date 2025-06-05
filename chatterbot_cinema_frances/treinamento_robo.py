import os

from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

from chatterbot_cinema_frances.robo import iniciar_robo 

_base_dir = os.path.dirname(__file__)

_CORPUS_DATA = (
    os.path.join(_base_dir, "dados_treinamento/comprimentos.yaml"),
    os.path.join(_base_dir, "dados_treinamento/conversas.yaml"),
)


def _treinar_com_corpus_data(treinador): # https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/portuguese
    for arquivo in _CORPUS_DATA:
        treinador.train(arquivo)

    print('Treinamento com arquivos de corpus finalizado!')



def main():
    chatbot = iniciar_robo()
    treinador_lista = ListTrainer(chatbot)
    treinador_corpus = ChatterBotCorpusTrainer(chatbot)

    _treinar_com_corpus_data(treinador_corpus)


if __name__ == "__main__":
    main()