"""
File runs all retrieval methods for demonstration.
"""

import time
from multiprocessing import freeze_support
import asyncio

from management.data_entry import DataCreator

if __name__ == '__main__':
    freeze_support()

    proces = DataCreator()

    start_time = time.perf_counter()
    proces.run_multiprocessing()
    end_time = time.perf_counter()
    print(f'Multiprocessing takes {end_time-start_time} seconds(s)')

    start_time = time.perf_counter()
    proces.run_threading()
    end_time = time.perf_counter()
    print(f'Threading takes {end_time-start_time} seconds(s)')

    start_time = time.perf_counter()
    asyncio.run(proces.run_concurrency())
    end_time = time.perf_counter()
    print(f'Concurrency takes {end_time-start_time} seconds(s)')
