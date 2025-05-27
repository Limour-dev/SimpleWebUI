import asyncio
import inspect
from threading import Thread

async def try_call(callback, args):
    try:
        task = callback(*args)
        if inspect.iscoroutine(task):
            task = await task
        return task
    except Exception as e:
        print(e)

class RunAfter:

    def event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        self.loop.close()

    def __init__(self, loop=None):
        if loop is None:
            self.loop = asyncio.new_event_loop()
            self.ep = Thread(target=self.event_loop, daemon=True)
            self.ep.start()
        else:
            self.loop = loop

    def __call__(self, intervals, callback, *args):
        task = try_call(callback, args)
        if intervals <= 0:
            return self.run(task)
        return self.loop.call_later(intervals, self.run, task)

    def run(self, task):
        return asyncio.run_coroutine_threadsafe(task, self.loop)
