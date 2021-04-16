import threading
import pymysql
from pycom.setting import MYSQL


class Store(object):
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.thread_local = threading.local()

    def __str__(self):
        return '{}:{}:{}'.format(type(self).__name__, self.host, self.user)

    def __repr__(self):
        return self.__str__()

    @property
    def con(self):
        con = getattr(self.thread_local, 'connection', None)
        if con:
            return con
        else:
            con = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.db,
                port=int(self.port),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            self.con = con
        return con

    @con.setter
    def con(self, v):
        self.thread_local.connection = v

    @property
    def trxing(self):
        return getattr(self.thread_local, 'trxing', False)

    @trxing.setter
    def trxing(self, v):
        self.thread_local.trxing = v

    def get_cursor(self):
        if not self.con:
            self.con = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.db,
                port=int(self.port),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
        if not self.trxing:
            self.con.ping(True)
        return self.con, self.con.cursor()

    def parse_execute_sql(self, sql):
        sql = sql.lstrip()
        cmd = sql.split(' ', 1)[0].lower()
        return cmd

    def execute(self, sql, *args, **kwargs):
        cmd = self.parse_execute_sql(sql)
        con, cursor = self.get_cursor()
        try:
            rs = cursor.execute(sql, args)
            if cmd in ['select', 'show']:
                return cursor.fetchall()
            elif cmd == 'insert':
                if kwargs.get('batch', False):
                    return list(range(cursor.lastrowid, cursor.lastrowid + cursor.rowcount))
                return cursor.lastrowid
            return rs
        except Exception:
            raise

    def begin(self):
        if self.con:
            self.con.ping()
            self.con.begin()

    def commit(self):
        if self.con:
            self.con.commit()

    def finish(self):
        pass

    def rollback(self):
        if self.con:
            self.con.rollback()


store = Store(
    host=MYSQL['host'],
    user=MYSQL['user'],
    password=MYSQL['password'],
    db=MYSQL['db'],
    port=MYSQL['port']
)