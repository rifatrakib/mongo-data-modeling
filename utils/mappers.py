import json

from beanie import WriteRules
from pymongo import MongoClient

from config import settings
from models.building_cases import Case, File, Journal, SingleCase


def map_data():
    with open("data/sample.json") as reader:
        data = json.loads(reader.read())

    results = []
    singles = []

    for doc in data:
        journals = []

        for journal in doc["JOURNALS"]:
            journal["FILES"] = [File(**file) for file in journal["FILES"]]
            journals.append(Journal(**journal))

        doc["JOURNALS"] = journals
        results.append(Case(**doc))
        singles.append(SingleCase(**doc))

    return results, singles


async def write_data():
    data, singles = map_data()
    SingleCase.insert_many(singles)

    for case in data:
        await case.save(link_rule=WriteRules.WRITE)


async def read_data():
    cases = await Case.find(Case.PROPERTY_ID_NMA == "4601-22-5-0-0", fetch_links=True).to_list()
    print(f"{cases = }")


def test_pymongo_query():
    client = MongoClient(settings.MONGO_URI)
    database = client["BUILDING_CASES"]
    collection = database["BUILDING_CASE_CASE_ID_PROPERTY_ID"]

    pipeline = [
        {"$match": {"PROPERTY_ID_NMA": "4601-22-5-0-0"}},
        {"$lookup": {"from": "BUILDING_CASE_CASE_ID_CASE_DICTS", "localField": "CASE_ID", "foreignField": "CASE_ID", "as": "case_data"}},
        {"$lookup": {"from": "BUILDING_CASE_JOURNAL_ID_CASE_ID", "localField": "CASE_ID", "foreignField": "CASE_ID", "as": "journals"}},
        {
            "$lookup": {
                "from": "BUILDING_CASE_JOURNAL_ID_JOURNAL_DICTS",
                "localField": "journals.JOURNAL_ID",
                "foreignField": "JOURNAL_ID",
                "as": "jounral_data",
            }
        },
        {
            "$lookup": {
                "from": "BUILDING_CASE_FILE_ID_JOURNAL_ID",
                "localField": "journals.JOURNAL_ID",
                "foreignField": "JOURNAL_ID",
                "as": "files",
            }
        },
        {
            "$lookup": {
                "from": "BUILDING_CASE_FILE_ID_FILE_DICTS",
                "localField": "files.FILE_ID",
                "foreignField": "FILE_ID",
                "as": "file_data",
            }
        },
    ]

    cases = list(collection.aggregate(pipeline, allowDiskUse=True))
    print(f"{cases = }")


async def test_single_collection_pattern():
    cases = await SingleCase.find(SingleCase.PROPERTY_ID_NMA == "4601-22-5-0-0").to_list()
    print(f"{cases = }")
