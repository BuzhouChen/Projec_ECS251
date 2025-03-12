import concurrent.futures
import requests
import time
import psutil

URLS = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.baidu.com"
] * 50  # 请求次数增加到200次

# 定义一个 URL 请求的函数
def fetch_url(url):
    try:
        response = requests.get(url, timeout=10)  # 设置请求的超时为10秒
        response.raise_for_status()  # 如果响应状态码不是 2xx，会抛出异常
        return f"{url}: {response.status_code}"
    except requests.Timeout:
        return f"{url}: Timeout error"
    except requests.ConnectionError:
        return f"{url}: Connection error"
    except requests.RequestException as e:
        return f"{url}: Error - {str(e)}"

# 获取性能指标：执行时间、吞吐量、CPU 使用率、内存使用量
def performance(executor_type, num_workers, task_num):
    start_time = time.time()
    process = psutil.Process()  
    initial_cpu = process.cpu_percent(interval=None)  
    initial_memory = process.memory_info().rss  

    execute(executor_type, num_workers, task_num)
    end_time = time.time()
    final_cpu = process.cpu_percent(interval=None)  
    final_memory = process.memory_info().rss  

    runtime = end_time - start_time
    throughput = task_num / runtime
    cpu = final_cpu - initial_cpu
    mem = final_memory - initial_memory

    return runtime, throughput, cpu, mem

# 执行任务的函数
def execute(executor, num_workers, task_num):
    with executor(max_workers=num_workers) as executor:
        futures = [executor.submit(fetch_url, url) for url in URLS[:task_num]]
        results = [future.result() for future in futures]

# 主函数
def main():
    task_num = 200  # 请求次数
    num_workers = 10  # 线程数或进程数

    print("Using ThreadPoolExecutor...")
    thread_time, thread_throughput, thread_cpu, thread_mem = performance(concurrent.futures.ThreadPoolExecutor, num_workers, task_num)
    print(f"Execution Time: {thread_time:.4f} s")
    print(f"Throughput: {thread_throughput:.4f} tasks/s")
    print(f"CPU usage: {thread_cpu:.2f}%")
    print(f"Memory usage: {thread_mem / (1024 ** 2):.2f} MB\n")

    print("Using ProcessPoolExecutor...")
    process_time, process_throughput, process_cpu, process_mem = performance(concurrent.futures.ProcessPoolExecutor, num_workers, task_num)
    print(f"Execution Time: {process_time:.4f} s")
    print(f"Throughput: {process_throughput:.4f} tasks/s")
    print(f"CPU usage: {process_cpu:.2f}%")
    print(f"Memory usage: {process_mem / (1024 ** 2):.2f} MB\n")

if __name__ == "__main__":
    main()


# Using ThreadPoolExecutor...
# Execution Time: 7.2311 s
# Throughput: 27.6582 tasks/s
# CPU usage: 12.50%
# Memory usage: 5.92 MB

# Using ProcessPoolExecutor...
# Execution Time: 9.3841 s
# Throughput: 21.3127 tasks/s
# CPU usage: 1.50%
# Memory usage: 0.42 MB