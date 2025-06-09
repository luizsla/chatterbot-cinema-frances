import os
import sqlite3

from contextlib import closing

_CREATE_SINOPSE_TABELA_QUERY = """
    CREATE TABLE IF NOT EXISTS sinopses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        info_adicional TEXT,
        sinopse TEXT,
        nome_arquivo TEXT
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
    INSERT INTO sinopses (titulo, info_adicional, sinopse, nome_arquivo) VALUES (?, ?, ?, ?);
"""

_GET_SINOPSE_QUERY = """
    SELECT id FROM sinopses ORDER BY id DESC LIMIT 1;
"""

_CREATE_TAGS_QUERY = """
    INSERT INTO tags (sinopse_id, tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

def build_select_sinopses_por_tags_query(tags): # Gerado com copilot
    """
    Gera a query SQL e os parâmetros para buscar sinopses que contenham todas as tags fornecidas.
    """
    base_query = """
        SELECT
            titulo,
            info_adicional,
            sinopse,
            nome_arquivo,
            t.tag_1,
            t.tag_2,
            t.tag_3,
            t.tag_4,
            t.tag_5,
            t.tag_6,
            t.tag_7
        FROM
            sinopses s
        JOIN tags t ON
            t.sinopse_id = s.id
    """
    if not tags:
        return base_query, []

    # Para cada tag, verifica se ela está em alguma das colunas de tags
    where_clauses = []
    params = []
    for tag in tags:
        clause = "(" + " OR ".join([f"t.tag_{i} = ?" for i in range(1, 8)]) + ")"
        where_clauses.append(clause)
        params.extend([tag] * 7)

    where_statement = " WHERE " + " OR ".join(where_clauses)
    final_query = base_query + where_statement

    return final_query, params


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



def gravar_sinopse(titulo, sinopse, info_adicional, nome_arquivo, tokens_sinopse):
    with closing(sqlite3.connect(_db_artigos)) as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(_CREATE_SINOPSE_QUERY, (titulo, info_adicional, sinopse, nome_arquivo))
            assert cursor.rowcount == 1, "Sinopse {} não pode ser criada".format(titulo)
            cursor.execute(_GET_SINOPSE_QUERY)
            id_ = cursor.fetchone()[0]
            cursor.execute(_CREATE_TAGS_QUERY, (id_, *tokens_sinopse))
            assert cursor.rowcount == 1, "Tags da sinopse {} não puderam ser criadas".format(titulo)
            conexao.commit()

    print("Gravando dados de: {}".format(titulo))



def buscar_sinopses_por_tags(tags):
    select_query, params = build_select_sinopses_por_tags_query(tags)
    with closing(sqlite3.connect(_db_artigos)) as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(select_query, params)
            resultados = cursor.fetchall()

    return [{
        "titulo": row[0],
        "info_adicional": row[1],
        "sinopse": row[2],
        "nome_arquivo": row[3],
        "tag_1": row[4],
        "tag_2": row[5],
        "tag_3": row[6],
        "tag_4": row[7],
        "tag_5": row[8],
        "tag_6": row[9],
        "tag_7": row[10]
    } for row in resultados]


if __name__ == "__main__":
    iniciar_db()