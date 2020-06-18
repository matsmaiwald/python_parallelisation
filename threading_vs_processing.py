import math
import time
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm


def run_cpu_bound_process(id: int):
    print(f"Starting cpu-bound process # {id}.")
    for i in range(1000, 4000):
        math.factorial(i)
    print(f"Finished cpu-bound process # {id}.")


def run_io_bound_process(id: int):
    print(f"Starting io-bound process # {id}")
    time.sleep(1)
    print(f"Finished io-bound process # {id}")


def main():
    # Define ids to keep track of processes
    id_numbers = list(range(1, 8))

    # Sequential runs
    print("-" * 20, "Starting sequential runs!", "-" * 20)

    t = time.time()
    for i in tqdm(id_numbers):
        run_cpu_bound_process(i)
    t_cpu_seq = time.time() - t

    t = time.time()
    for i in tqdm(id_numbers):
        run_io_bound_process(i)
    t_io_seq = time.time() - t

    # Multi-process runs
    print("-" * 20, "Starting multi-process runs!", "-" * 20)

    t = time.time()
    pool = Pool(cpu_count())
    list(tqdm(pool.imap(run_cpu_bound_process, id_numbers), total=len(id_numbers)))
    pool.close()
    pool.join()
    t_cpu_proc = time.time() - t
    t = time.time()

    pool = Pool(cpu_count())
    list(tqdm(pool.imap(run_io_bound_process, id_numbers), total=len(id_numbers)))
    pool.close()
    pool.join()
    t_io_proc = time.time() - t

    # Multi-thread runs
    print("-" * 20, "Starting multi-thread runs!", "-" * 20)

    t = time.time()
    pool = ThreadPool(8)
    pool.map(run_cpu_bound_process, id_numbers)
    t_cpu_thread = time.time() - t

    t = time.time()
    pool = ThreadPool(8)
    pool.map(run_io_bound_process, id_numbers)
    t_io_thread = time.time() - t

    # Comparing run times
    print("-" * 30)
    print("--- Sequential run time cpu-bound task: {} seconds ---".format(t_cpu_seq))
    print(
        "--- Multi-process run time cpu-bound task: {} seconds ---".format(t_cpu_proc)
    )
    print(
        "--- Multi-thread run time cpu-bound task: {} seconds ---".format(t_cpu_thread)
    )

    print("-" * 30)
    print("--- Sequential run time io-bound task: {} seconds ---".format(t_io_seq))
    print("--- Multi-process run time io-bound task: {} seconds ---".format(t_io_proc))
    print("--- Multi-thread run time io-bound task: {} seconds ---".format(t_io_thread))

    print("-" * 30)


if __name__ == "__main__":
    main()
