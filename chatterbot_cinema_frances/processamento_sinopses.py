import os
import yaml


_diretorio_arquivos = os.path.join(os.path.dirname(__file__), "sinopses_filmes")

_NUMERO_MAX_ARTIGOS = 52


def main():
    for contador in range(1, _NUMERO_MAX_ARTIGOS):
        arquivo_sinopse = os.path.join(_diretorio_arquivos, "%d.yaml" % contador)
        with open(arquivo_sinopse, 'r', encoding="utf-8") as arquivo:
            dados_sinopse = yaml.load(arquivo, Loader=yaml.SafeLoader)

            print(dados_sinopse)


if __name__ == "__main__":
    main()