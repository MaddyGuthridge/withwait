"""
Main implementation for withwait
"""
from types import TracebackType
from typing import ContextManager
from time import time, sleep


class wait(ContextManager):
    def __init__(self, seconds: float) -> None:
        """Withwait

        Ensure the timer always finishes, even if an exception happens for code
        inside a with statement

        Args:
            seconds (float): number of seconds to wait
        """
        self.__seconds = seconds
        # Set when entering context manager
        self.__start_time: float = 0

    def __enter__(self) -> None:
        self.__start_time = time()

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None
    ) -> None:
        time_to_sleep = self.__seconds - (time() - self.__start_time)
        # Wait the remaining required time if needed
        if time_to_sleep > 0:
            sleep(time_to_sleep)
