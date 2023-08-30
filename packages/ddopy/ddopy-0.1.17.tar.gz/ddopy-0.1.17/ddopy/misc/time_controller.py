from datetime import timedelta
from datetime import datetime
from datetime import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class TimeController:
    def __init__(self) -> None:
        self.__remaining_time = 0
        self.__current_time = 0
        self.__scheduler = None

    def start(self, duration):
        self.__remaining_time = duration
        self.__current_time = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.start()
        self.add_periodic_job(self.__on_every_second, 1)

    def stop(self):
        self.__remaining_time = 0

    def add_periodic_job(self, method, interval):
        self.__scheduler.add_job(
            method,
            "interval",
            seconds=interval,
            id=method.__name__,
            replace_existing=True,
        )

        assert self.has_periodic_job(method)

    def has_periodic_job(self, method):
        return self.__scheduler.get_job(method.__name__) is not None

    def remove_periodic_job(self, method):
        if self.has_periodic_job(method):
            self.__scheduler.remove_job(method.__name__)

        assert not self.has_periodic_job(method)

    def get_periodic_job_interval(self, method):
        result = 0

        if self.has_periodic_job(method):
            result = self.__scheduler.get_job(method.__name__).trigger.interval.seconds

        return result

    async def __on_every_second(self):
        self.__current_time += timedelta(seconds=1)
        self.__remaining_time -= 1

        if self.__remaining_time <= 0:
            self.__scheduler.shutdown()

    def get_current_time(self):
        return self.__current_time.astimezone().isoformat()

    def set_current_time(self, current_time):
        self.__current_time = current_time

    def get_remaining_time(self):
        return self.__remaining_time
