import asyncio

class TaskManager:
    def __init__(self):
        self.running_tasks = set()

    async def run_task(self, async_func, *args, **kwargs):
        task = asyncio.create_task(async_func(*args, **kwargs))
        self.running_tasks.add(task)
        task.add_done_callback(lambda t: self.running_tasks.remove(t))