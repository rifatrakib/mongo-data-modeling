import asyncio

from utils.clients import pool_database_clients
from utils.downloader import download_files
from utils.mappers import read_data, test_pymongo_query, test_single_collection_pattern, write_data
from utils.processing import create_dataframes, process_json_files


async def initial_ops():
    download_files()
    process_json_files()
    create_dataframes()

    await pool_database_clients()
    await write_data()
    await read_data()
    test_pymongo_query()
    await test_single_collection_pattern()


if __name__ == "__main__":
    asyncio.run(initial_ops())
