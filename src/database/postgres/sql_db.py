import asyncpg

sql_db = None

async def connect_pg():
    global sql_db
    sql_db = await asyncpg.connect(user='no-brainer-db', password='no-brainer-db',
                                 database='no-brainer-db', host='127.0.0.1', port=8907)
    print('connect to postgres')
    return sql_db

async def close_pg():
    global sql_db
    await sql_db.close()
    print('close postgres')
