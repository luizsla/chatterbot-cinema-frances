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

_db_artigos = os.path.join(os.path.dirname(__file__), "sinopses.sqlite")


def _iniciar_db():
    if os.path.exists(_db_artigos):
        os.remove(_db_artigos)

    with closing(sqlite3.connect(_db_artigos)) as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(_CREATE_SINOPSE_TABELA_QUERY)
            cursor.execute(_CREATE_TAGS_TABELA_QUERY)
            conexao.commit()



if __name__ == "__main__":
    _iniciar_db()