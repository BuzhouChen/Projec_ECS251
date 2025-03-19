from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import psutil

# Fibonacci function
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# get the performance metrics
# runtime, throughput, cpu, memory
# executor_type: ThreadPoolExecutor or ProcessPoolExecutor
def performance(executor_type, num_workers, task_num):
    start_time = time.time()
    process = psutil.Process()  
    initial_memory = process.memory_info().rss  

    execute(executor_type, num_workers, task_num)
    end_time = time.time()
    final_memory = process.memory_info().rss  
    runtime = end_time - start_time
    throughput = task_num / runtime
    mem = final_memory - initial_memory

    return runtime, throughput, mem

def execute(executor, num_workers, task_num):
    with executor(max_workers=num_workers) as executor:
        futures = [executor.submit(fibonacci, 30) for _ in range(task_num)]
        results = [future.result() for future in futures]
        cpu_usage = psutil.cpu_percent(interval=0)
    return cpu_usage

def main():
    task_num = 500  # number of tasks
    num_workers = 4  # number of threads/processes

    print("ThreadPoolExecutor:")
    thread_time, thread_throughput, thread_mem = performance(ThreadPoolExecutor, num_workers, task_num)
    thread_cpu = execute(ThreadPoolExecutor, num_workers, task_num)
    print(f"Execution Time: {thread_time:.4f} s")
    print(f"Throughput: {thread_throughput:.4f} tasks/s")
    print(f"CPU usage: {thread_cpu:.2f}%")
    print(f"Memory usage: {thread_mem / (1024 ** 2):.2f} MB\n")

    print("ProcessPoolExecutor:")
    process_time, process_throughput, process_mem = performance(ProcessPoolExecutor, num_workers, task_num)
    process_cpu = execute(ProcessPoolExecutor, num_workers, task_num)
    print(f"Execution Time: {process_time:.4f} s")
    print(f"Throughput: {process_throughput:.4f} tasks/s")
    print(f"CPU usage: {process_cpu:.2f}%")
    print(f"Memory usage: {process_mem / (1024 ** 2):.2f} MB\n")


if __name__ == "__main__":
    main()