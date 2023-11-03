from datetime import datetime
from typing import Any, Dict, List, Union

from beanie import Document, Indexed, Link


class File(Document):
    FILE_NAME: str
    FILE_TYPE: Union[str, None] = None
    FILE_URL: Union[str, None] = None
    FILE_CONTENT_TYPE: Union[str, None] = None


class Journal(Document):
    JOURNAL_DATE: Union[datetime, None] = None
    JOURNAL_TITLE: str
    JOURNAL_LINK: Union[str, None] = None
    FILES: List[Link[File]]


class Case(Document):
    PROPERTY_ID_NMA: Indexed(str)
    CASE_TITLE: str
    CASE_URL: Union[str, None] = None
    CASE_TYPE: Union[str, None] = None
    CASE_START_DATE: Union[datetime, None] = None
    CASE_CLOSE_DATE: Union[datetime, None] = None
    JOURNALS: List[Link[Journal]]


class SingleCase(Document):
    PROPERTY_ID_NMA: Indexed(str)
    CASE_TITLE: str
    CASE_URL: Union[str, None] = None
    CASE_TYPE: Union[str, None] = None
    CASE_START_DATE: Union[datetime, None] = None
    CASE_CLOSE_DATE: Union[datetime, None] = None
    JOURNALS: List[Dict[str, Any]]
