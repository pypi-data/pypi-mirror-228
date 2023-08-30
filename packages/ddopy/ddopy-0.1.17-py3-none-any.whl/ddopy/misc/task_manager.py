import asyncio


class TaskManager:
    def __init__(self, async_func, *args, **kwargs):
        self.running_tasks = set()
        task = asyncio.create_task(async_func(*args, **kwargs))
        self.running_tasks.add(task)
        task.add_done_callback(lambda t: self.running_tasks.remove(t))
