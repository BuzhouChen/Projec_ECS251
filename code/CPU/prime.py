import random
import time
import psutil
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n: 
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_numbers(num_tasks, min_value=10**12, max_value=10**15):
    return [random.randint(min_value, max_value) for _ in range(num_tasks)]

def measure_performance(executor, task, inputs):
    
    start_time = time.time()
    process = psutil.Process()  
    initial_cpu = process.cpu_percent(interval=None)  
    initial_memory = process.memory_info().rss  
    
    with executor(max_workers=4) as executor:
        results = list(executor.map(task, inputs))
    
    end_time = time.time()
    final_cpu = process.cpu_percent(interval=None)  
    final_memory = process.memory_info().rss  
    
    elapsed_time = end_time - start_time
    throughput = len(inputs) / elapsed_time  

    print(f"{type(executor).__name__} time: {elapsed_time:.2f} s")
    print(f"{type(executor).__name__} throughput: {throughput:.2f} tasks/sec")
    print(f"{type(executor).__name__} CPU usage: {final_cpu - initial_cpu:.2f}%")
    print(f"{type(executor).__name__} Memory usage: {(final_memory - initial_memory) / (1024 ** 2):.2f} MB\n")

def main():
    num_tasks = 1000 
    numbers = generate_numbers(num_tasks)

    print(f"ThreadPoolExecutor:")
    measure_performance(ThreadPoolExecutor, is_prime, numbers)

    print(f"ProcessPoolExecutor:")
    measure_performance(ProcessPoolExecutor, is_prime, numbers)

if __name__ == "__main__":
    main()
