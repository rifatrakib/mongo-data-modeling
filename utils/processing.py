import json

import pandas as pd


def process_json_files():
    names = {
        "BUILDING_CASE_CASE_ID_CASE_DICTS": ["CASE_START_DATE", "CASE_CLOSE_DATE"],
        "BUILDING_CASE_JOURNAL_ID_JOURNAL_DICTS": ["JOURNAL_DATE"],
    }

    for name, fields in names.items():
        with open(f"data/{name}.json", "r") as reader:
            data = json.loads(reader.read())

        for doc in data:
            for field in fields:
                if doc[field]:
                    doc[field] = doc[field]["$date"]

        with open(f"data/{name}.json", "w") as writer:
            writer.write(json.dumps(data, indent=4))


def create_dataframes():
    results = []

    map_df = pd.read_json("data/BUILDING_CASE_CASE_ID_PROPERTY_ID.json")
    data_df = pd.read_json("data/BUILDING_CASE_CASE_ID_CASE_DICTS.json")
    data_df = data_df.drop_duplicates(["CASE_ID"], keep="first")

    case_df = data_df.merge(map_df, on="CASE_ID", how="inner")
    case_df = case_df.drop_duplicates(ignore_index=True)

    map_df = pd.read_json("data/BUILDING_CASE_JOURNAL_ID_CASE_ID.json")
    data_df = pd.read_json("data/BUILDING_CASE_JOURNAL_ID_JOURNAL_DICTS.json")

    journal_df = data_df.merge(map_df, on="JOURNAL_ID", how="inner")
    journal_df = journal_df.drop_duplicates(ignore_index=True)

    map_df = pd.read_json("data/BUILDING_CASE_FILE_ID_JOURNAL_ID.json")
    data_df = pd.read_json("data/BUILDING_CASE_FILE_ID_FILE_DICTS.json")

    file_df = data_df.merge(map_df, on="FILE_ID", how="inner")
    file_df = file_df.drop_duplicates(ignore_index=True)

    for row in range(case_df.shape[0]):
        case = case_df.iloc[row]
        data = case.to_dict()
        journals = journal_df[journal_df.CASE_ID == case.CASE_ID].to_dict(orient="records")

        for journal in journals:
            files = file_df[file_df.JOURNAL_ID == journal["JOURNAL_ID"]].to_dict(orient="records")
            journal["FILES"] = files

        data["JOURNALS"] = journals
        results.append(data)

    with open("data/sample.json", "w") as writer:
        writer.write(json.dumps(results, indent=4))
