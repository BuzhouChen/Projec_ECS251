from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Fibonacci function
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# get the execution time and throughput
def performance(executor, num_workers, task_num):
    start_time = time.time()
    execute(executor, num_workers, task_num)
    end_time = time.time()
    time = end_time - start_time
    throughput = task_num / time

    return time, throughput

def execute(executor, num_workers, task_num):
    with executor(max_workers=num_workers) as executor:
        futures = [executor.submit(fibonacci, 30) for _ in range(task_num)]
        results = [future.result() for future in futures]

def main():
    task_num = 20  # number of tasks
    num_workers = 4  # number of threads/processes

    print("ThreadPoolExecutor:")
    thread_time, thread_throughput = performance(ThreadPoolExecutor, num_workers, task_num)
    print(f"Execution Time: {thread_time:.4f} s")
    print(f"Throughput: {thread_throughput:.4f} tasks/s\n")

    print("ProcessPoolExecutor:")
    process_time, process_throughput = performance(ProcessPoolExecutor, num_workers, task_num)
    print(f"Execution Time: {process_time:.4f} s")
    print(f"Throughput: {process_throughput:.4f} tasks/s\n")


if __name__ == "__main__":
    main()