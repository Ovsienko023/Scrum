from typing import Any, Optional, List

import aiopg
import psycopg2
from aiopg.pool import Pool
from psycopg2.extras import RealDictCursor

from internal.database.errors import ErrorDatabase


class ClientDB:
    _host: str = None
    _port: int = None
    _user: str = None
    _password: str = None
    _database: str = None
    _pool: Optional[Pool] = None

    def __init__(self,
                 host: str or None = None,
                 port: int or None = None,
                 user: str or None = None,
                 password: str or None = None,
                 database: str or None = None):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database

    async def is_connected(self) -> bool:
        try:
            await self.fetchone("SELECT 1")
            return True
        except (Exception, psycopg2.DatabaseError):

            return False

    async def fetchone(self, query: Any, parameters: Any = None, timeout: Optional[Any] = None):
        try:
            await self._reconnect()
            connection: aiopg.Connection = await self._pool.acquire()
            cursor: aiopg.Cursor = await connection.cursor(cursor_factory=RealDictCursor)
            await cursor.execute(query, parameters=parameters, timeout=timeout)
            res = await cursor.fetchone()
            await self._release(connection)
            return res
        except Exception as exc:
            raise ErrorDatabase(exc)

    async def fetchall(self, query: Any, parameters: Any = None, timeout: Optional[Any] = None) -> List:
        try:
            await self._reconnect()
            connection: aiopg.Connection = await self._pool.acquire()
            cursor: aiopg.Cursor = await connection.cursor(cursor_factory=RealDictCursor)
            await cursor.execute(query, parameters=parameters, timeout=timeout)
            res = await cursor.fetchall()
            await self._release(connection)
            return res
        except Exception as exc:
            raise ErrorDatabase(exc)

    async def _reconnect(self):
        if self._pool is None or self._pool.closed is True:
            self._pool: Pool = await aiopg.create_pool(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database,
                maxsize=5
            )

    async def connect(self):
        if not self._pool:
            self._pool: Pool = await aiopg.create_pool(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database,
                maxsize=5
            )

    async def _release(self, connection):
        if connection in self._pool._used:
            await self._pool.release(connection)

    async def close(self):
        if self._pool is None:
            return None

        return self._pool.close()
