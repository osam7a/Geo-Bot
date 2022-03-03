import aiosqlite
import asyncio


class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass


class DBmember(aobject):
    async def __init__(self, id, table, conn):
        self.id, self.table = id, table
        self.conn = conn
        cursor = await self.conn.cursor()
        await cursor.execute(f"SELECT * FROM {self.table} WHERE id={self.id}")
        a = await cursor.fetchall()
        if len(a) == 0:
            await self.openAccount()
        await cursor.close()

    async def openAccount(self):
        cursor = await self.conn.cursor()
        await cursor.execute(f"INSERT INTO {self.table} (id, warns, prefix) VALUES ({self.id}, 0, \"geo \")")
        await self.conn.commit()
        await cursor.close()

    @property
    async def warns(self):
        cursor = await self.conn.cursor()
        await cursor.execute(f"SELECT warns FROM {self.table} WHERE id={self.id}")
        a = await cursor.fetchall()
        await cursor.close()
        warns = a[0][0]
        return warns

    @warns.setter
    async def warn(self, other):
        cursor = await self.conn.cursor()
        await cursor.execute(f"UPDATE {self.table} SET warns={other} WHERE id={self.id}")
        await self.conn.commit()
        await cursor.close()

class Database:
    def __init__(self, file, table, tableArgs):
        self.file = file
        self.table = table
        self.tableArgs = tableArgs

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(f"src/databases/{self.file}")
        cursor = await self.conn.cursor()
        await cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table}{self.tableArgs}")
        await self.conn.commit()
        await cursor.close()
        return self

    async def getMember(self, id):
        return await DBmember(id, self.table, self.conn)

    async def __aexit__(self, var, var2, var3):
        await self.conn.close()
