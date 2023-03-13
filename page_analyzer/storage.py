from psycopg2 import connect
from psycopg2.extras import DictCursor


GET_URL_ID_BY_NAME_QUERY = "SELECT id FROM urls WHERE name = %(name)s;"
ADD_NEW_URL_QUERY = """INSERT INTO urls (name)
                       VALUES (%(name)s)
                       RETURNING id, name, created_at;"""
GET_URL_BY_ID_QUERY = "SELECT id, name, created_at FROM urls WHERE id = %(id)s;"
GET_URLS_QUERY = """SELECT id, name,
                           NULL as last_checked_at, NULL as status_code
                    FROM urls ORDER BY created_at DESC;"""


class UrlExists(Exception):
    def __init__(self, id):
        super().__init__()
        self.id = id


class URLStorage:

    def __init__(self, dsn):
        self._conn = connect(dsn=dsn)

    def _fetch(self, query, many=False, **query_args):
        with self._conn as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, query_args)
                if many:
                    return cursor.fetchmany()
                else:
                    return cursor.fetchone()

    def _get_id_by_name(self, name):
        return self._fetch(GET_URL_ID_BY_NAME_QUERY, name=name)

    def add(self, name):
        existing_url = self._get_id_by_name(name)
        if existing_url:
            raise UrlExists(existing_url["id"])
        return self._fetch(ADD_NEW_URL_QUERY, name=name)

    def get(self, id):
        return self._fetch(GET_URL_BY_ID_QUERY, id=id)

    def list(self):
        return self._fetch(GET_URLS_QUERY, many=True)
