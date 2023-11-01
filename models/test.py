from typing import List

from beanie import Document, Link


class TestRoot(Document):
    name: str
    description: str
    amount: int
    price: float
    subs: List[Link["TestSubLevel1"]]


class TestSubLevel1(Document):
    name: str
    description: str
    amount: int
    price: float
    subs: List[Link["TestSubLevel2"]]


class TestSubLevel2(Document):
    name: str
    description: str
    amount: int
    price: float
    subs: List[Link["TestSubLevel3"]]


class TestSubLevel3(Document):
    name: str
    description: str
    amount: int
    price: float
