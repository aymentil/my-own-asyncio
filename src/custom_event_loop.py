from asyncio import AbstractEventLoop, Handle, TimerHandle
from collections import deque
from bisect import insort
from typing import Any, Callable
import time

class MyEventLoop(AbstractEventLoop):
    def __init__(self):
        self._ready_handles = deque[Handle]()
        self._scheduled_handles = deque[TimerHandle]()
        self._should_stop = False

    def call_soon(
            self, callback: Callable, *args: Any
    ) -> Handle:
        handle = Handle(callback=callback, args=args, loop=self)
        self._ready_handles.append(handle)
        return handle

    def call_at(
            self, when: float, callback: Callable, *args: Any
    ) -> TimerHandle:
        timer_handle = TimerHandle(
            when=when, callback=callback, args=args, loop=self
        )
        print(f'Created timer handle {timer_handle}')
        insort(self._scheduled_handles, timer_handle)
        timer_handle._scheduled = True

        return timer_handle
    
    def time():
        return time.monotonic()
    
    def get_debug(self) -> bool:
        return True


    def call_later(
            self, delay: float, callback: Callable, *args: Any
    ) -> TimerHandle:
        return self.call_at(
            when=self.time() + delay,
            callback=callback,
            *args
        )

    def _run_once(self):
        now = time.time()
        while (
            len(self._scheduled_handles) > 0
            and self._scheduled_handles[0].when() <= now
        ):
            handle = self._scheduled_handles.popleft()
            self._ready_handles.append(handle)
            print(f"Running handle = {handle}")
            handle._run()
        
        while len(self._ready_handles) > 0:
            handle = self._ready_handles.popleft()
            print(f"Running handle {handle}")
            handle._run()


    def run_forever(self):
        while not self._should_stop:
            self._run_once()
