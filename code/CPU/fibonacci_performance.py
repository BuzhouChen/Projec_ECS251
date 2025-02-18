import concurrent.futures
import time
import psutil

def cpu_bound_task(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def create_task_collection():
    cpu_tasks = [n for n in range(30, 80)] 
    return cpu_tasks

def get_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    return cpu_percent, memory_percent

# task execution
def execute_tasks(pool_type, tasks, num_repeats=1):
    start_time = time.time()
    initial_cpu, initial_memory = get_system_metrics()
    if pool_type == 'thread':
        results = execute_in_thread_pool(tasks, num_repeats)
    elif pool_type == 'process':
        results = execute_in_process_pool(tasks, num_repeats)
    final_cpu, final_memory = get_system_metrics()

    execution_time = time.time() - start_time
    task_latencies = [result[1] - result[0] for result in results]
    throughput = len(tasks) * num_repeats / execution_time if execution_time > 0 else 0

    print(f"Execution Time: {execution_time:.2f} seconds")
    print(f"CPU Utilization: {final_cpu - initial_cpu:.2f}%")
    print(f"Memory Utilization: {final_memory - initial_memory:.2f}%")
    print(f"Average Task Completion Latency: {sum(task_latencies)/len(task_latencies):.2f} seconds")
    print(f"Throughput: {throughput:.2f} tasks per second")

    return results

def execute_in_thread_pool(tasks, num_repeats):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        start_times = []  
        for task in tasks:
            for _ in range(num_repeats): 
                start_time = time.time()
                futures.append(executor.submit(cpu_bound_task, task))  
                start_times.append(start_time)

        results = [(start_times[i], future.result()) for i, future in enumerate(concurrent.futures.as_completed(futures))]
    return results

def execute_in_process_pool(tasks, num_repeats):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        start_times = [] 
        for task in tasks:
            for _ in range(num_repeats): 
                start_time = time.time()
                futures.append(executor.submit(cpu_bound_task, task)) 
                start_times.append(start_time)

        results = [(start_times[i], future.result()) for i, future in enumerate(concurrent.futures.as_completed(futures))]
    return results

if __name__ == '__main__':
    cpu_tasks = create_task_collection()
    print("Thread Pool:")
    cpu_results_thread = execute_tasks('thread', cpu_tasks, num_repeats=1)
    print("\nProcess Pool:")
    cpu_results_process = execute_tasks('process', cpu_tasks, num_repeats=1)
