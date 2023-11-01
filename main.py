import asyncio

from utils.clients import pool_database_clients

if __name__ == "__main__":
    asyncio.run(pool_database_clients())
