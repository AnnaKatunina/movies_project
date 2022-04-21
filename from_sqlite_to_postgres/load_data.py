import os
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from dataclasses_movies import Person, Genre, Filmwork, GenreFilmwork, PersonFilmwork
from loader_and_saver import SQLiteLoader, PostgresSaver

load_dotenv()

TABLES_CLASSES = [
    {'table': 'person', 'dataclass': Person},
    {'table': 'genre', 'dataclass': Genre},
    {'table': 'film_work', 'dataclass': Filmwork},
    {'table': 'genre_film_work', 'dataclass': GenreFilmwork},
    {'table': 'person_film_work', 'dataclass': PersonFilmwork}
]

ROW_AMOUNT = 100


@contextmanager
def open_db(file_name: str):
    conn = sqlite3.connect(file_name)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    sqlite_cursor = connection.cursor()
    pg_cursor = pg_conn.cursor()
    postgres_saver = PostgresSaver(pg_cursor)
    sqlite_loader = SQLiteLoader(sqlite_cursor)

    for table_class in TABLES_CLASSES:
        data = sqlite_loader.load_data(table_class['table'], table_class['dataclass'], ROW_AMOUNT)
        postgres_saver.save_data(data, table_class['table'], table_class['dataclass'])


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432)
    }
    with open_db('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
