from psycopg2 import connect
from psycopg2.extras import DictCursor


GET_URL_ID_BY_NAME_QUERY = "SELECT id FROM urls WHERE name = %(name)s;"
ADD_NEW_URL_QUERY = """INSERT INTO urls (name)
                       VALUES (%(name)s)
                       RETURNING id, name, created_at;"""
GET_URL_BY_ID_QUERY = """SELECT urls.id as url_id,
                                urls.name as url_name,
                                urls.created_at as url_created_at,
                                url_checks.id as id,
                                url_checks.status_code as status_code,
                                url_checks.h1 as h1,
                                url_checks.title as title,
                                url_checks.description as description,
                                url_checks.created_at as created_at
                         FROM urls
                         LEFT JOIN url_checks ON urls.id = url_checks.url_id
                         WHERE urls.id = %(id)s;"""
GET_URLS_QUERY = """SELECT DISTINCT ON (id)
                           urls.id as id,
                           urls.name as name,
                           url_checks.created_at as last_checked_at,
                           url_checks.status_code as status_code
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    ORDER BY id DESC, url_checks.created_at DESC;"""
ADD_URL_CHECK = """INSERT INTO url_checks (url_id, status_code)
                   VALUES (%(id)s, %(status_code)s)
                   RETURNING id;"""


class UrlExists(Exception):
    def __init__(self, id):
        super().__init__()
        self.id = id


class UrlNotFound(Exception):
    pass


class URLStorage:

    def __init__(self, dsn):
        self._conn = connect(dsn=dsn)

    def _execute(self, query, return_many=False, **query_args):
        with self._conn as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, query_args)
                if return_many:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()

    def _get_id_by_name(self, name):
        return self._execute(GET_URL_ID_BY_NAME_QUERY, name=name)

    def add(self, name):
        existing_url = self._get_id_by_name(name)
        if existing_url:
            raise UrlExists(existing_url["id"])
        return self._execute(ADD_NEW_URL_QUERY, name=name)

    def get(self, id):
        result = self._execute(GET_URL_BY_ID_QUERY, id=id, return_many=True)
        if not result:
            raise UrlNotFound
        first_result = result[0]
        return {
            "id": first_result["url_id"],
            "name": first_result["url_name"],
            "created_at": first_result["url_created_at"],
            "checks": result if first_result["id"] else []
        }

    def list(self):
        return self._execute(GET_URLS_QUERY, return_many=True)

    def add_url_check(self, id, status_code):
        return self._execute(ADD_URL_CHECK, id=id, status_code=status_code)
