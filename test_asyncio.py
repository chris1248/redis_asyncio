from unittest import IsolatedAsyncioTestCase
import pytest
import asyncio
import redis as syncredis
import redis.asyncio


class Testit(IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n---setupClass---")
        sync_client = syncredis.Redis(host="127.0.0.1", port=6379)
        sync_client.flushall()
        sync_client.close()

    def setUp(self):
        self.addAsyncCleanup(self.on_cleanup)
        print("\nsetUp")

    async def asyncSetUp(self):
        print("asyncSetUp")
        self.client = redis.asyncio.Redis(host="127.0.0.1", port=6379)
        Testit.curr_loop = asyncio.get_running_loop()
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")
        print(f"\tloop is closed: {Testit.curr_loop.is_closed()}")

    async def test_response_one(self):
        print("TEST_ONE")
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")
        print(f"\tloop is closed: {Testit.curr_loop.is_closed()}")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("Luke","Luke Skywalker")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}")

    async def test_response_two(self):
        print("TEST_TWO")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("Princess","Princess Leia")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}") 
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")

    async def test_response_three(self):
        print("TEST_THREE")
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")
        print(f"\tloop is closed: {Testit.curr_loop.is_closed()}")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("R2","R2D2 droid unit")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")

    def tearDown(self):
        print("tearDown")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")

    async def asyncTearDown(self):
        print("asyncTearDown")
        await self.client.close()
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")

    async def on_cleanup(self):
        print("cleanup")
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")
        print(f"\tloop is closed: {Testit.curr_loop.is_closed()}")

    @classmethod
    def tearDownClass(cls) -> None:
        print("\n---TearDownClass---")
        print(f"\tloop is running: {cls.curr_loop.is_running()}")
        return super().tearDownClass()

