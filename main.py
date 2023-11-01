import asyncio

from beanie import WriteRules

from models.test import TestRoot, TestSubLevel1, TestSubLevel2, TestSubLevel3
from utils.clients import pool_database_clients


async def initial_ops():
    await pool_database_clients()

    level_3_sub_1 = TestSubLevel3(name="test_sub_1", description="test_sub_1", amount=1, price=1.0)
    level_3_sub_2 = TestSubLevel3(name="test_sub_2", description="test_sub_2", amount=2, price=2.0)
    level_3_sub_3 = TestSubLevel3(name="test_sub_3", description="test_sub_3", amount=3, price=3.0)

    level_2_sub_1 = TestSubLevel2(name="test_sub_1", description="test_sub_1", amount=1, price=1.0, subs=[level_3_sub_1])
    level_2_sub_2 = TestSubLevel2(name="test_sub_2", description="test_sub_2", amount=2, price=2.0, subs=[level_3_sub_2])
    level_2_sub_3 = TestSubLevel2(name="test_sub_3", description="test_sub_3", amount=3, price=3.0, subs=[level_3_sub_3])

    level_1_sub_1 = TestSubLevel1(name="test_sub_1", description="test_sub_1", amount=1, price=1.0, subs=[level_2_sub_1, level_2_sub_3])
    level_1_sub_2 = TestSubLevel1(name="test_sub_2", description="test_sub_2", amount=2, price=2.0, subs=[level_2_sub_2, level_2_sub_3])
    level_1_sub_3 = TestSubLevel1(
        name="test_sub_3", description="test_sub_3", amount=3, price=3.0, subs=[level_2_sub_1, level_2_sub_2, level_2_sub_3]
    )

    root_1 = TestRoot(name="test_root_1", description="test_root_1", amount=1, price=1.0, subs=[level_1_sub_1, level_1_sub_2])
    root_2 = TestRoot(name="test_root_2", description="test_root_2", amount=2, price=2.0, subs=[level_1_sub_2, level_1_sub_3])

    await root_1.save(link_rule=WriteRules.WRITE)
    await root_2.save(link_rule=WriteRules.WRITE)

    item = await TestRoot.find_one(TestRoot.name == "test_root_2", fetch_links=True)
    print(item.model_dump())


if __name__ == "__main__":
    asyncio.run(initial_ops())
