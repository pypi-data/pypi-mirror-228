from databricks import sql

class DatabricksSQLClient:
    def __init__(self, server_hostname: str, http_path: str, access_token: str):
        self._server_hostname = server_hostname
        self._http_path = http_path
        self._token = access_token

    def execute_statement(self, statement: str):
        with sql.connect(server_hostname=self._server_hostname,
                         http_path=self._http_path,
                         access_token=self._token) as connection:

            with connection.cursor() as cursor:
                cursor.execute(statement)
                return cursor.fetchall_arrow()