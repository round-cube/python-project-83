from psycopg2 import connect
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation


class UrlExists(Exception):
    def __init__(self, id):
        super().__init__()
        self.id = id


class URLStorage:
    def __init__(self, dsn):
        self._conn = connect(dsn=dsn)

    def _get_id_by_name(self, name):
        with self._conn as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT id FROM urls WHERE name = (%s);", (name,))
                return cursor.fetchone()

    def add(self, name):
        existing_url = self._get_id_by_name(name)
        if existing_url:
            raise UrlExists(existing_url["id"])

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
