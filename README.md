# Project_ECS251  

## Aims

Our project will address these issues through a systematic benchmarking study of Python’s `ThreadPoolExecutor`. Specifically, we will:

- Analyze the impact of the GIL on threading performance by comparing `ThreadPoolExecutor` with `ProcessPoolExecutor` for different workloads (I/O-bound, CPU-bound, and mixed).
- Investigate thread pool size optimization by testing different pool sizes under various conditions (e.g., fixed size vs. adaptive scaling).
- Evaluate scheduling policies (FIFO, LIFO, priority queue, round-robin) by implementing custom scheduling mechanisms and measuring their impact on task completion time, throughput, and fairness.


## Works  

In the folder `code` is the different workloads that we are going to run. Codes are devided into different subfolders according to their types.  

## Platform 

To ensure consistency and eliminate performance variations caused by different hardware, we run our code on Google Colab. But Jupyter Notebook cannot run ProcessPoolExecutor properly, so we eventually run the code on our laptops.

## Results

+ ThreadPoolExecutor is effective for I/O-bound tasks but limited by the GIL for CPU-bound tasks.
ProcessPoolExecutor outperforms thread pools for CPU-bound tasks but has higher overhead and can fail for I/O-bound tasks.
+ ThreadPoolExecutor seems to be more effective for mixed workloads.
+ Creating and managing processes has higher overhead compared to threads.
+ Optimal thread pool size depends on the workload and system resources.
+ For CPU-bound tasks, the optimal pool size is usually set to the number of available CPU cores to maximize parallelism without excessive context switching
+ In general, ProcessPoolExecutor struggles with certain objects and processes, such as machine learning classification (torchvision). 

## Tips   

Jupyter Notebook cannot run `ProcessPoolExecutor` properly because it uses multiple processes, which causes issues with how Jupyter handles multiprocessing. Jupyter runs in an interactive environment, and when ProcessPoolExecutor tries to spawn new processes, it can cause problems with the underlying process management, such as not being able to properly share resources between processes. This often results in the notebook hanging or crashing. To use `ProcessPoolExecutor` effectively, it's recommended to run the code outside of Jupyter, such as in a regular Python script or through a terminal.
