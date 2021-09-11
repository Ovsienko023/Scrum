import psycopg2


class ClientDB:
    """Creating a connection to the database."""
    def __init__(self, dbname, user, password, host, port):
        # self.info_db = self.get_info_db()
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def query(self, request):
        self._reconnect()
        self.cur.execute(request)
        self.conn.commit()

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()

    def status(self):
        return self.cur.statusmessage

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def _reconnect(self):
        if not self.conn:
            self.connect()
        if self.cur.closed:
            self.connect()

    def close(self):
        self.conn.close()
