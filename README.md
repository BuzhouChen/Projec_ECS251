# Projec_ECS251  

## Aims

Our project will address these issues through a systematic benchmarking study of Python’s `ThreadPoolExecutor`. Specifically, we will:

- Analyze the impact of the GIL on threading performance by comparing `ThreadPoolExecutor` with `ProcessPoolExecutor` for different workloads (I/O-bound, CPU-bound, and mixed).
- Investigate thread pool size optimization by testing different pool sizes under various conditions (e.g., fixed size vs. adaptive scaling).
- Evaluate scheduling policies (FIFO, LIFO, priority queue, round-robin) by implementing custom scheduling mechanisms and measuring their impact on task completion time, throughput, and fairness.


## Works  

In the folder `code` is the different workloads that we are going to run. Codes are devided into different subfolders according to their types.  

## Platform 

To ensure consistency and eliminate performance variations caused by different hardware, we run our code on Google Colab.
