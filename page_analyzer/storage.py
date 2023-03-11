from psycopg2 import connect
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation


class UrlExists(Exception):
    pass


class URLStorage:
    def __init__(self, dsn):
        self._conn = connect(dsn=dsn)

    def add(self, name):
        with self._conn as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id, name, created_at;", (name,))
                return cursor.fetchone()

    def get(self, id):
        with self._conn as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('SELECT id, name, created_at FROM urls WHERE id = %s;', (id,))
                return cursor.fetchone()

    def list(self):
        with self._conn as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('SELECT id, name, NULL as last_checked_at, NULL as status_code FROM urls ORDER BY created_at DESC;')
                return cursor.fetchall()
