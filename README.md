# Background
While trying to get async-redis to work I ran into issues while writing unit tests for it.
This code for this git repo boils down the code to it's most basic parts.

# Prerequisites
1. This assumes you have python 3.9 installed on your machine. If you don't then simply edit setup_venv.sh and give it a different python version.
2. This assumes you have the virtualenv package installed (via brew).
3. This assumes you have the redis cli installed. So you can run `redis-server` for instance.

# How to build
1. Open a terminal window
2. Run the command `./setup_venv.sh`
3. Run the command `source venv/bin/activate`

# How to run all the tests
1. Run the command `redis-server`
2. First build the code (see steps above)
3. Run the command `make unit-tests`

# Problem with tests:
When running all the tests at one time using pytest, some will fail with errors that look like this:
```
       # Waiting for data while paused will make deadlock, so prevent it.
        # This is essential for readexactly(n) for case when n > self._limit.
        if self._paused:
            self._paused = False
            self._transport.resume_reading()

        self._waiter = self._loop.create_future()
        try:
>           await self._waiter
E           RuntimeError: Task <Task pending name='Task-3' coro=<IsolatedAsyncioTestCase._asyncioLoopRunner() running at /usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/unittest/async_case.py:101> created at /usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/unittest/async_case.py:117> got Future <Future pending created at /usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncio/base_events.py:424> attached to a different loop

/usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncio/streams.py:517: RuntimeError

During handling of the above exception, another exception occurred:

self = <test_asyncio.Testit testMethod=test_response_three>

    async def test_response_three(self):
        print("TEST_THREE")
        async with self.client.pipeline(transaction=False) as pipeline:
            pipeline.set("gideon","Gideon Johnson")
            pipeline.keys("*")
>           result = await pipeline.execute()

test_asyncio.py:62:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
venv/lib/python3.9/site-packages/redis/asyncio/client.py:1352: in execute
    return await conn.retry.call_with_retry(
venv/lib/python3.9/site-packages/redis/asyncio/retry.py:59: in call_with_retry
    return await do()
venv/lib/python3.9/site-packages/redis/asyncio/client.py:1266: in _execute_pipeline
    await self.parse_response(connection, args[0], **options)
venv/lib/python3.9/site-packages/redis/asyncio/client.py:1291: in parse_response
    result = await super().parse_response(connection, command_name, **options)
venv/lib/python3.9/site-packages/redis/asyncio/client.py:505: in parse_response
    response = await connection.read_response()
venv/lib/python3.9/site-packages/redis/asyncio/connection.py:943: in read_response
    await self.disconnect()
venv/lib/python3.9/site-packages/redis/asyncio/connection.py:828: in disconnect
    self._writer.close()  # type: ignore[union-attr]
/usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncio/streams.py:353: in close
    return self._transport.close()
/usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncio/selector_events.py:700: in close
    self._loop.call_soon(self._call_connection_lost, None)
/usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncio/base_events.py:746: in call_soon
    self._check_closed()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <_UnixSelectorEventLoop running=False closed=True debug=True>

    def _check_closed(self):
        if self._closed:
>           raise RuntimeError('Event loop is closed')
E           RuntimeError: Event loop is closed

/usr/local/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncio/base_events.py:510: RuntimeError

```
