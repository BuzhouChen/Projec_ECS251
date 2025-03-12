import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# import concurrent.futures
import time
import psutil

# 读取文件内容
def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# 写入文件内容
def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

# 统一测试函数
def performance(executor_type, num_workers, task, file_list, out_file_list=None):
    start_time = time.time()
    process = psutil.Process()
    initial_cpu = process.cpu_percent(interval=None)
    initial_memory = process.memory_info().rss

    if task == "read":
        results = execute(executor_type, num_workers, read_file, file_list)
    elif task == "write":
        results = execute(executor_type, num_workers, write_file, file_list, out_file_list)
    else:
        raise ValueError("Unknown task type. Use 'read' or 'write'.")

    end_time = time.time()
    final_cpu = process.cpu_percent(interval=None)
    final_memory = process.memory_info().rss

    runtime = end_time - start_time
    throughput = len(file_list) / runtime
    cpu = final_cpu - initial_cpu
    mem = (final_memory - initial_memory) / (1024 ** 2)  # MB

    return runtime, throughput, cpu, mem

# 统一执行函数
def execute(executor_type, num_workers, func, file_list, out_file_list=None):
    with executor_type(max_workers=num_workers) as executor:
        if out_file_list:
            executor.map(func, file_list, out_file_list)  # 适用于写文件（有两个参数）
        else:
            return list(executor.map(func, file_list))  # 适用于读文件（只有一个参数）

# 主函数
def main():
    file_list = [f"./data/big_file_{i}.txt" for i in range(10)]
    out_file_list = [f"./data/output_{i}.txt" for i in range(len(file_list))]
    num_workers = 5

    print("ThreadPoolExecutor (READ):")
    thread_read_time, thread_read_throughput, thread_read_cpu, thread_read_mem = performance(ThreadPoolExecutor, num_workers, "read", file_list)
    print(f"Execution Time: {thread_read_time:.2f} s | Throughput: {thread_read_throughput:.2f} tasks/s")
    print(f"CPU usage: {thread_read_cpu:.2f}% | Memory usage: {thread_read_mem:.2f} MB\n")

    print("ProcessPoolExecutor (READ):")
    process_read_time, process_read_throughput, process_read_cpu, process_read_mem = performance(ProcessPoolExecutor, num_workers, "read", file_list)
    print(f"Execution Time: {process_read_time:.2f} s | Throughput: {process_read_throughput:.2f} tasks/s")
    print(f"CPU usage: {process_read_cpu:.2f}% | Memory usage: {process_read_mem:.2f} MB\n")

    print("ThreadPoolExecutor (WRITE):")
    thread_write_time, thread_write_throughput, thread_write_cpu, thread_write_mem = performance(ThreadPoolExecutor, num_workers, "write", file_list, out_file_list)
    print(f"Execution Time: {thread_write_time:.2f} s | Throughput: {thread_write_throughput:.2f} tasks/s")
    print(f"CPU usage: {thread_write_cpu:.2f}% | Memory usage: {thread_write_mem:.2f} MB\n")

    print("ProcessPoolExecutor (WRITE):")
    process_write_time, process_write_throughput, process_write_cpu, process_write_mem = performance(ProcessPoolExecutor, num_workers, "write", file_list, out_file_list)
    print(f"Execution Time: {process_write_time:.2f} s | Throughput: {process_write_throughput:.2f} tasks/s")
    print(f"CPU usage: {process_write_cpu:.2f}% | Memory usage: {process_write_mem:.2f} MB\n")

if __name__ == "__main__":
    main()

# ThreadPoolExecutor (READ):
# Execution Time: 0.37 s | Throughput: 27.31 tasks/s
# CPU usage: 493.40% | Memory usage: 1000.24 MB

# ProcessPoolExecutor (READ):
# Execution Time: 2.07 s | Throughput: 4.84 tasks/s
# CPU usage: 71.50% | Memory usage: 1000.42 MB


# ThreadPoolExecutor (WRITE):
# Execution Time: 0.11 s | Throughput: 87.70 tasks/s
# CPU usage: 0.00% | Memory usage: 0.03 MB

# ProcessPoolExecutor (WRITE):
# Execution Time: 0.32 s | Throughput: 31.34 tasks/s
# CPU usage: 15.40% | Memory usage: 0.02 MB