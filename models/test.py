from beanie import Document


class Test(Document):
    name: str
    description: str
    amount: int
    price: float
