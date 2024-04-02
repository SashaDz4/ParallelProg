from mpi4py import MPI
import random


def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y >>= 1
        x = (x * x) % p
    return res


def miillerTest(d, n, a):
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


def isPrime(n, k, a_list):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for a in a_list:
        if not miillerTest(d, n, a):
            return False
    return True


def master(num1, k, comm):
    num_processes = comm.Get_size()
    results = []

    # Distribute workload among processes
    workload_per_process = k // num_processes
    a_list = [2 + random.randint(1, num1 - 4) for _ in range(k)]  # Generate a list of random bases

    # Send workload and bases to worker processes
    for i in range(1, num_processes):
        comm.send((num1, workload_per_process, a_list), dest=i)

    # Master process performs its own share of workload
    result = isPrime(num1, workload_per_process, a_list[:workload_per_process])
    results.append(result)

    # Receive results from worker processes
    for i in range(1, num_processes):
        result = comm.recv(source=i)
        results.extend(result)

    return all(results)


def worker(comm):
    while True:
        rank = comm.Get_rank()
        num1, workload, a_list = comm.recv(source=0)

        # Worker process performs its share of workload
        results = [isPrime(num1, workload, a_list[rank * workload:(rank + 1) * workload])]

        comm.send(results, dest=0)


if __name__ == "__main__":
    import time

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_processes = comm.Get_size()

    if rank == 0:
        num1 = 2305843009213693951
        k1 = 100000
        start = time.time()
        master(num1, k1, comm)
        end = time.time()
        print(f"Time taken for {k1:.1e} iterations with {num_processes} processes: {end - start:.2f} seconds")

        k2 = 1000000
        start = time.time()
        master(num1, k2, comm)
        end = time.time()
        print(f"Time taken for {k2:.1e} iterations with {num_processes} processes: {end - start:.2f} seconds")

    else:
        worker(comm)
