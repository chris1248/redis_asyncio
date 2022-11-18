from unittest import IsolatedAsyncioTestCase
import pytest
import asyncio
import redis as syncredis
import redis.asyncio

def _print_loop_info():
    curr_loop = asyncio.get_running_loop()
    print(f"\tLoop: {id(curr_loop)}, running: {curr_loop.is_running()}, closed: {curr_loop.is_closed()}")
    return curr_loop

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
        # There is no access to the event loop here. So we cannot call async functions here.

    async def asyncSetUp(self):
        print("asyncSetUp")
        self.client = redis.asyncio.Redis(host="127.0.0.1", port=6379)
        _print_loop_info()

    async def test_response_one(self):
        print("TEST_ONE")
        _print_loop_info()
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
        _print_loop_info()
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("Princess","Princess Leia")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}") 

    async def test_response_three(self):
        print("TEST_THREE")
        _print_loop_info()
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("R2","R2D2 droid unit")
            pipeline.keys("*")
            result = await pipeline.execute()
            names = result[1:][0]
            for r in names:
                if type(r) is not bool:
                    print(f"\tname: {r.decode()}")

    def tearDown(self):
        print("tearDown")
        # There is no access to the event loop here. So we cannot call async functions here.

    async def asyncTearDown(self):
        print("asyncTearDown")
        await self.client.close()
        _print_loop_info()

    async def on_cleanup(self):
        print("cleanup")
        _print_loop_info()

    @classmethod
    def tearDownClass(cls) -> None:
        print("\n---TearDownClass---")
        return super().tearDownClass()
        _print_loop_info()

