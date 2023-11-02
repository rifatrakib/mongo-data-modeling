import boto3


def download_files():
    names = [
        "BUILDING_CASE_CASE_ID_CASE_DICTS",
        "BUILDING_CASE_CASE_ID_PROPERTY_ID",
        "BUILDING_CASE_FILE_ID_FILE_DICTS",
        "BUILDING_CASE_FILE_ID_JOURNAL_ID",
        "BUILDING_CASE_JOURNAL_ID_CASE_ID",
        "BUILDING_CASE_JOURNAL_ID_JOURNAL_DICTS",
    ]

    client = boto3.client("s3", region_name="eu-north-1")

    for name in names:
        client.download_file(
            "data-general",
            f"sandbox/BUILDING_CASE_SAMPLE_DATA_FROM_STAGING_CLUSTER_DB/{name}.json",
            f"data/{name}.json",
        )
