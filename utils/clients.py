from typing import Dict, List, Union

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from models.test import Test


def database_collection_mappers() -> List[Dict[str, Union[str, List[Document]]]]:
    return [
        {
            "database": "realestate",
            "document_models": [Test],
        },
    ]


async def pool_database_clients():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    mappers = database_collection_mappers()

    for mapper in mappers:
        mapper["database"] = client[mapper.get("database")]
        await init_beanie(**mapper)
