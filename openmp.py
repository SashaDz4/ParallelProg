import random
import time
import multiprocessing


def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y >>= 1
        x = (x * x) % p
    return res


def miillerTest(d, n):
    a = 2 + random.randint(1, n - 4)
    x = power(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def isPrime_worker(n, k, result_queue):
    for _ in range(k):
        if not miillerTest(n - 1, n):
            result_queue.put(False)
            return
    result_queue.put(True)


def isPrime(n, k, num_processes):
    num_processes += 1
    processes = []
    result_queue = multiprocessing.Queue()

    for _ in range(num_processes):
        p = multiprocessing.Process(target=isPrime_worker, args=(n, k // num_processes, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Collect results
    results = [result_queue.get() for _ in range(num_processes)]

    return all(results)


def print_result(num, k, num_process):
    num_process += 1
    start = time.time()
    isPrime(num, k, num_process)
    end = time.time()
    # write k with 1en format
    print(f"Time taken for {k:.1e} iterations with {num_process} processes: {end - start:.2f} seconds")


if __name__ == "__main__":
    num1 = 2305843009213693951
    k1 = 100000
    k2 = 1000000
    # benchmarking
    for num_processes in range(6):
        print_result(num1, k1, num_processes)
        print_result(num1, k2, num_processes)
