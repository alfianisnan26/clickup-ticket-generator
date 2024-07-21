import queue
import threading
import time
from typing import Callable, Any

from logger import logger


class RateLimiter:
    def __init__(self, rate: float):
        self.rate = rate
        self.last_time = time.time()
        self.lock = threading.Lock()

    def wait(self) -> None:
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.last_time
            wait_time = max(0, 1.0 / self.rate - elapsed)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_time = time.time()


class ThreadPoolLimiter:
    def __init__(self, num_threads: int, rate: float):
        self.queue = queue.Queue()
        self.threads = []
        self.rate_limiter = RateLimiter(rate)
        self.shutdown_flag = threading.Event()
        self.queue_lock = threading.Lock()

        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self) -> None:
        while not self.shutdown_flag.is_set() or not self.queue.empty():
            try:
                task, args, kwargs = self.queue.get(timeout=1)
                if task is None:
                    continue
                self.rate_limiter.wait()
                task(*args, **kwargs)
                self.queue.task_done()
            except queue.Empty:
                continue

    def submit(self, task: Callable[..., None], *args: Any, **kwargs: Any) -> None:
        with self.queue_lock:
            self.queue.put((task, args, kwargs))

    def wait_until_finish(self, cooldown_period: float = 10.0) -> None:
        logger.debug("Waiting for the queue to be empty and cooldown period...")

        while True:
            cooldown_start = time.time()
            with self.queue_lock:
                if self.queue.empty():
                    logger.debug("Queue is empty. Starting cooldown period of %s seconds...", cooldown_period)
                else:
                    logger.debug("Queue is not empty. Checking again in 3 seconds.")
                    time.sleep(3)
                    continue

            while time.time() - cooldown_start < cooldown_period:
                with self.queue_lock:
                    if not self.queue.empty():
                        logger.debug("New tasks detected. Resetting cooldown period.")
                        break

                time.sleep(1)  # Check if new tasks are added every second

            else:
                # Cooldown completed without new tasks
                logger.debug("Cooldown period finished. Proceeding to shutdown.")
                break

        # Signal threads to shut down
        logger.debug("Signaling threads to shut down.")
        self.shutdown_flag.set()

        # Join remaining threads
        logger.debug("Joining remaining threads.")
        for thread in self.threads:
            thread.join()
        logger.debug("All threads have been joined.")


# Example usage
if __name__ == "__main__":
    import random

    def example_task(arg1: int, arg2: str) -> None:
        logger.info(f"Task with arguments ({arg1}, {arg2}) executed at {time.time()}")
        if random.random() > 0.5:
            # Example of submitting a new task
            thread_pool.submit(example_task, arg1 + 1, arg2 + "!")


    thread_pool = ThreadPoolLimiter(num_threads=3, rate=2.0)

    for _ in range(10):
        thread_pool.submit(example_task, random.randint(1, 100), "example")
        time.sleep(random.uniform(0, 1))

    thread_pool.wait_until_finish()
