import concurrent.futures
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import time
import psutil
from image_gen import pick_random_image_path, generate_white_noise_image

# function for image classification (via torchvision ResNet18 model)
def classify_image(image_path):
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    model.eval()
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(image)
    return output.argmax().item()

# function for measuring CPU and memory usage
def get_resource_usage():
    process = psutil.Process()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_info = process.memory_info().rss / (1024 * 1024)
    return cpu_percent, memory_info
    
# function to classify images using ThreadPoolExecutor
def process_with_threadpool(files):
    start_time = time.time()                      # start timer
    cpu_start, mem_start = get_resource_usage()   # CPU and memory usage at the start
    
    # classify images with ThreadPool
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(classify_image, files))
    
    end_time = time.time()                        # end timer
    cpu_end, mem_end = get_resource_usage()       # CPU and memory usage at the end
    
    # calculate metrics based on difference
    total_time = end_time - start_time
    throughput = len(files) / total_time
    cpu_usage = cpu_end - cpu_start
    mem_usage = mem_end - mem_start

    return results, total_time, throughput, cpu_usage, mem_usage

# function to classify images using ProcessPoolExecutor
def process_with_processpool(files):
    start_time = time.time()                      # start timer
    cpu_start, mem_start = get_resource_usage()   # CPU and memory usage at the start
    
    # classify images with ProcessPool
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(classify_image, files))
    
    end_time = time.time()                        # end timer
    cpu_end, mem_end = get_resource_usage()       # CPU and memory usage at the end
    
    # calculate metrics based on difference
    total_time = end_time - start_time
    throughput = len(files) / total_time
    cpu_usage = cpu_end - cpu_start
    mem_usage = mem_end - mem_start

    return results, total_time, throughput, cpu_usage, mem_usage   

if __name__ == "__main__":        # idiom to prevent program freeze for processes
    
    # randomly picking high res image
    high_res_image_path = pick_random_image_path("high-res-images")
    print(f"\nChoosing high res image {high_res_image_path[-5]}.")

    # randomly picking low res image
    low_res_image_path = pick_random_image_path("low-res-images")
    print(f"Choosing low res image {low_res_image_path[-5]}.")

    # generating white noise image
    white_noise_image_path = generate_white_noise_image()
    if white_noise_image_path:
        print("Successfully generated white noise image.")

    # defining image paths
    image_paths = [high_res_image_path, low_res_image_path, white_noise_image_path]
    
    # call function for ThreadPoolExecutor
    thread_results, thread_time, thread_throughput, thread_cpu, thread_mem = process_with_threadpool(image_paths)
    
    # call function for ProcessPoolExecutor
    process_results, process_time, process_throughput, process_cpu, process_mem = process_with_processpool(image_paths)

    # display ThreadPoolExecutor metrics for user
    print(f"\nThreadPoolExecutor results: {thread_results}")
    print(f"ThreadPoolExecutor time: {thread_time:.4f} seconds")
    print(f"ThreadPoolExecutor throughput: {thread_throughput:.4f} images/sec")
    print(f"ThreadPoolExecutor CPU usage: {thread_cpu:.2f}%")
    print(f"ThreadPoolExecutor memory usage: {thread_mem:.2f} MB")

    # display ProcessPoolExecutor metrics for user
    print(f"\nProcessPoolExecutor results: {process_results}")
    print(f"ProcessPoolExecutor time: {process_time:.4f} seconds")
    print(f"ProcessPoolExecutor throughput: {process_throughput:.4f} images/sec")
    print(f"ProcessPoolExecutor CPU usage: {process_cpu:.2f}%")
    print(f"ProcessPoolExecutor memory usage: {process_mem:.2f} MB")