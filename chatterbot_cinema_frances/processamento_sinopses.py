import os
import yaml

from collections import Counter
from string import punctuation
from nltk import word_tokenize, corpus
from nltk.corpus import floresta

from chatterbot_cinema_frances.database import iniciar_db, gravar_sinopse


_diretorio_arquivos = os.path.join(os.path.dirname(__file__), "sinopses_filmes")

_NUMERO_MAX_ARTIGOS = 52

_CLASSES_GRAMATICAIS_INDESEJADAS = (
    "adv",
    "v-inf", 
    'v-fin',
    "v-pcp",
    "v-ger",
    "num"
)


def _extrair_titulo(dados_sinopse):
    return dados_sinopse["filme"]



def _extrair_sinopse(dados_sinopse):
    return dados_sinopse["sinopse"]



def _extrair_info_adicional(dados_sinopse):
    return "Diretor: %(diretor)s - Ano: %(ano)d - Roteiro: %(roteiro)s" % dados_sinopse



def _eliminar_palavras_de_parada(tokens):
    palavras_de_parada = set(corpus.stopwords.words("portuguese"))

    return tuple(token for token in tokens if token not in palavras_de_parada)



def _eliminar_caracteres_especiais(tokens):
    return tuple(token for token in tokens if token not in punctuation)



def _get_classificacoes_de_palavras():
    classificacoes = {}
    for palavra, classificacao in floresta.tagged_words():
        classificacoes[palavra.lower()] = classificacao

    return classificacoes



def _eliminar_classes_gramaticais_indesejadas(tokens):
    classificacoes = _get_classificacoes_de_palavras()

    tokens_filtrados = []
    for token in tokens:
        if token in classificacoes:
            classificacao = classificacoes[token]
            if not any(s in classificacao for s in _CLASSES_GRAMATICAIS_INDESEJADAS):
                tokens_filtrados.append(token)
        else:
            tokens_filtrados.append(token)

    return tokens_filtrados



def _filtrar_por_tokens_mais_presentes(tokens, n=7):
    contador = Counter(tokens)
    # Retorna os n tokens mais comuns e suas contagens
    return tuple(palavra for palavra, _ in contador.most_common(n))



def _processar_sinopse_filme(sinopse):
    tokens = word_tokenize(sinopse.lower())
    tokens_sem_palavras_parada = _eliminar_palavras_de_parada(tokens)
    tokens_sem_caracteres_especiais = _eliminar_caracteres_especiais(tokens_sem_palavras_parada)
    tokens_gramaticalmente_limpos =  _eliminar_classes_gramaticais_indesejadas(
        tokens_sem_caracteres_especiais
    )
    tokens_mais_frequentes = _filtrar_por_tokens_mais_presentes(tokens_gramaticalmente_limpos)

    return tokens_mais_frequentes



def main():
    iniciar_db()

    for contador in range(1, _NUMERO_MAX_ARTIGOS):
        arquivo_sinopse = os.path.join(_diretorio_arquivos, "%d.yaml" % contador)
        with open(arquivo_sinopse, 'r', encoding="utf-8") as arquivo:
            dados_sinopse = yaml.load(arquivo, Loader=yaml.SafeLoader)
            titulo = _extrair_titulo(dados_sinopse)
            sinopse = _extrair_sinopse(dados_sinopse)
            info_adicional = _extrair_info_adicional(dados_sinopse)
            tokens_sinopse = _processar_sinopse_filme(sinopse)
            assert len(tokens_sinopse) == 7, "Todas às sinopses devem ter 7 tags"

            gravar_sinopse(titulo, sinopse, info_adicional, tokens_sinopse)


if __name__ == "__main__":
    main()