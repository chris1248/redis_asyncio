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
        cls.client = redis.asyncio.Redis(host="127.0.0.1", port=6379)
        sync_client = syncredis.Redis(host="127.0.0.1", port=6379)
        sync_client.flushall()
        sync_client.close()

    def setUp(self):
        self.client = Testit.client
        self.addAsyncCleanup(self.on_cleanup)
        print("\nsetUp")

    async def asyncSetUp(self):
        print("asyncSetUp")
        Testit.curr_loop = asyncio.get_running_loop()
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")
        print(f"\tloop is closed: {Testit.curr_loop.is_closed()}")

    async def test_response_one(self):
        print("TEST_ONE")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("haydon","Haydon Johnson")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}")
        print(f"\tLoop: {id(Testit.curr_loop)}")
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")
        print(f"\tloop is closed: {Testit.curr_loop.is_closed()}")

    async def test_response_two(self):
        print("TEST_TWO")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("hannah","Hannah Johnson")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}") 
        print(f"\tloop is running: {Testit.curr_loop.is_running()}")

    async def test_response_three(self):
        print("TEST_THREE")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("gideon","Gideon Johnson")
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

