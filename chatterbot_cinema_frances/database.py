import os
import sqlite3

from contextlib import closing

_CREATE_SINOPSE_TABELA_QUERY = """
    CREATE TABLE IF NOT EXISTS sinopses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        info_adicional TEXT,
        sinopse TEXT
    );
"""

_CREATE_TAGS_TABELA_QUERY = """
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sinopse_id INTEGER,
        tag_1 TEXT,
        tag_2 TEXT,
        tag_3 TEXT,
        tag_4 TEXT,
        tag_5 TEXT,
        tag_6 TEXT,
        tag_7 TEXT,
        FOREIGN KEY (sinopse_id) REFERENCES sinopses(id)
    );
"""

_CREATE_SINOPSE_QUERY = """
    INSERT INTO sinopses (titulo, info_adicional, sinopse) VALUES (?, ?, ?);
"""

_GET_SINOPSE_QUERY = """
    SELECT id FROM sinopses ORDER BY id DESC LIMIT 1;
"""

_CREATE_TAGS_QUERY = """
    INSERT INTO tags (sinopse_id, tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

_db_artigos = os.path.join(os.path.dirname(__file__), "sinopses.sqlite")


def iniciar_db():
    if os.path.exists(_db_artigos):
        os.remove(_db_artigos)

    with closing(sqlite3.connect(_db_artigos)) as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(_CREATE_SINOPSE_TABELA_QUERY)
            cursor.execute(_CREATE_TAGS_TABELA_QUERY)
            conexao.commit()
    
    print("Banco de dados iniciado com sucesso!")



def gravar_sinopse(titulo, sinopse, info_adicional, tokens_sinopse):
    with closing(sqlite3.connect(_db_artigos)) as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(_CREATE_SINOPSE_QUERY, (titulo, info_adicional, sinopse))
            assert cursor.rowcount == 1, "Sinopse {} não pode ser criada".format(titulo)
            cursor.execute(_GET_SINOPSE_QUERY)
            id_ = cursor.fetchone()[0]
            cursor.execute(_CREATE_TAGS_QUERY, (id_, *tokens_sinopse))
            assert cursor.rowcount == 1, "Tags da sinopse {} não puderam ser criadas".format(titulo)
            conexao.commit()

    print("Gravando dados de: {}".format(titulo))


if __name__ == "__main__":
    iniciar_db()