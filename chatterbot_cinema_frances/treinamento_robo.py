import json
import os

from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

from chatterbot_cinema_frances.robo import iniciar_robo 

_base_dir = os.path.dirname(__file__)

_CORPUS_DATA = (
    os.path.join(_base_dir, "dados_treinamento/comprimentos.yaml"),
    os.path.join(_base_dir, "dados_treinamento/conversas.yaml"),
)
_LISTAS_TREINO = (
    os.path.join(_base_dir, "dados_treinamento/solicitacoes_roteiro.json"),
)


def _treinar_com_corpus_data(treinador): # https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/portuguese
    for arquivo in _CORPUS_DATA:
        treinador.train(arquivo)

    print('Treinamento com arquivos de corpus finalizado!')



def _treinar_com_lista(treinador):
    for arquivo in _LISTAS_TREINO:
        with open(arquivo, 'r') as arquivo_aberto:
            json_arquivo = json.load(arquivo_aberto)
            for conversa in json_arquivo["conversas"]:
                resposta = conversa["resposta"]
                for mensagem in conversa["mensagens"]:
                    treinador.train([mensagem, resposta])



def main():
    chatbot = iniciar_robo()
    chatbot.storage.drop()
    treinador_lista = ListTrainer(chatbot)
    treinador_corpus = ChatterBotCorpusTrainer(chatbot)

    _treinar_com_corpus_data(treinador_corpus)
    _treinar_com_lista(treinador_lista)


if __name__ == "__main__":
    main()