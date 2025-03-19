# Some possible examples.  

## **1. I/O-Bound Workloads (Best Fit for ThreadPoolExecutor)**  

### **Example 1: Web Scraping with ThreadPoolExecutor**  
Simulating multiple concurrent HTTP requests to fetch web pages.  

```python
import concurrent.futures
import requests

URLS = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.stackoverflow.com"
] * 5  # Simulate multiple requests

def fetch_url(url):
    response = requests.get(url)
    return f"{url}: {response.status_code}"

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, URLS))

for result in results:
    print(result)
```
**Metrics to Measure:**  
- Average response time per request  
- Total time taken with different thread pool sizes  

---

### **Example 2: Concurrent File Reading and Writing**  
Reading from multiple large text files and writing results concurrently.  

```python
import concurrent.futures

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_file(data, filename):
    with open(filename, 'w') as f:
        f.write(data)

files = ["file1.txt", "file2.txt", "file3.txt"]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    contents = list(executor.map(read_file, files))

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(write_file, contents, ["output1.txt", "output2.txt", "output3.txt"])
```
**Metrics to Measure:**  
- Time taken for reading and writing  
- Effect of increasing/decreasing `max_workers`  

---

## **2. CPU-Bound Workloads (Limited by GIL, Favoring ProcessPoolExecutor)**  

### **Example 3: Fibonacci Calculation (Heavy CPU Task)**  
Calculating Fibonacci numbers recursively to stress the CPU.  

```python
import concurrent.futures

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

numbers = [30, 32, 34, 36]

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fibonacci, numbers))

print(results)
```
**Alternative:** Running the same workload with **ProcessPoolExecutor** instead of ThreadPoolExecutor to check if it performs better.  

```python
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fibonacci, numbers))
```
**Metrics to Measure:**  
- Execution time under `ThreadPoolExecutor` vs. `ProcessPoolExecutor`  
- CPU utilization  

---

### **Example 4: Prime Number Check**  
Checking if large random numbers are prime to simulate a CPU intensive workload.  

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import random
import time

def is_prime(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

numbers = [random.randint(10**12, 10**15) for _ in range(1000)]

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(is_prime, numbers)

with ProcessPoolExecutor(max_workers=4) as executor:
    executor.map(is_prime, numbers)
```
**Metrics to Measure:**  
- Compression time across different thread pool sizes  
- Compare ThreadPoolExecutor vs. ProcessPoolExecutor  

---

## **3. Mixed Workloads (Combination of CPU and I/O Tasks)**  

### **Example 5: Image Processing & Saving (CPU + I/O)**  
Resizing images and saving them concurrently.  

```python
import concurrent.futures
from PIL import Image

def process_image(filename):
    img = Image.open(filename)
    img = img.resize((100, 100))
    img.save("resized_" + filename)

image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_image, image_files)
```
**Metrics to Measure:**  
- Processing time for different numbers of worker threads  
- Memory and CPU usage  

---

### **Example 6: Machine Learning Inference (Batch Predictions in Parallel)**  
Using a pre-trained deep learning model to classify images concurrently.  

```python
import concurrent.futures
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

# Load a pre-trained ResNet model
model = models.resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def classify_image(image_path):
    img = Image.open(image_path)
    img = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(img)
    return output.argmax().item()

image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(classify_image, image_paths))

print(results)
```
**Metrics to Measure:**  
- Latency per inference  
- Performance with different thread pool sizes  

---

## **4. Scheduling Policies Comparison**  
We will also test **FIFO, LIFO, Priority Queue, and Round-Robin** scheduling policies by modifying how tasks are assigned to worker threads.  

### **Example 7: Priority Queue for Task Scheduling**  
Using a priority queue where **high-priority tasks execute first**.  

```python
import concurrent.futures
import heapq

tasks = [
    (1, "Low Priority Task"),
    (3, "High Priority Task"),
    (2, "Medium Priority Task")
]

def execute_task(task):
    priority, description = task
    print(f"Executing: {description}")

tasks = sorted(tasks, reverse=True)  # Simulate priority queue

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(execute_task, tasks)
```
**Metrics to Measure:**  
- Task completion order under different scheduling strategies  
- Effect of scheduling on overall execution time  

---

## **Summary of Workloads and Their Purpose**  

| **Workload** | **Type** | **Why It Matters?** |
|-------------|----------|---------------------|
| Web Scraping | I/O-Bound | Tests thread pool efficiency for network-bound tasks |
| File I/O | I/O-Bound | Measures disk read/write concurrency |
| Fibonacci Calculation | CPU-Bound | Highlights GIL impact, compares ProcessPoolExecutor |
| Data Compression | CPU-Bound | Tests parallel compression performance |
| Image Processing | Mixed | Evaluates both CPU and I/O workload efficiency |
| ML Inference | Mixed | Tests deep learning inference with multiple threads |
| Priority Queue Scheduling | Scheduling | Evaluates custom scheduling impact on task execution |

