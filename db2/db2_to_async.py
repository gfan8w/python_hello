import asyncio
from concurrent.futures import ThreadPoolExecutor

# import ibm_db_dbi as db2

_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='db2')
#
# async def run_query():  # can be invoked concurrently
#     def do():
#         conn: db2.Connection = db2.pconnect(dsn='...')
#         with conn.cursor() as cursor:
#             cursor.execute('select 1+1 from SYSIBM.SYSDUMMY1')
#             result = cursor.fetchone()
#         conn.close()
#         return result
#
#     return await asyncio.get_event_loop().run_in_executor(_executor, do)

# print(await run_query())  # does not block the event loop
# print(await run_query())  # does not block the event loop
# print(await run_query())  # does not block the event loop