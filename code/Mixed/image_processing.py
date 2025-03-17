# import necessary libraries
import concurrent.futures
from PIL import Image
import time
import psutil
from image_gen import pick_random_image_path, generate_white_noise_image

# function for image processing (loading, resizing, and saving)
def process_image(image_path):
    image = Image.open(image_path)
    image = image.resize((100, 100))
    image.save("resized_" + image_path)
    
# function for measuring CPU and memory usage
def get_resource_usage():
    process = psutil.Process()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_info = process.memory_info().rss / (1024 * 1024)
    return cpu_percent, memory_info

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

    
    # ThreadPoolExecutor
    start_time = time.time()                      # start timer
    cpu_start, mem_start = get_resource_usage()   # CPU and memory usage at the start

    # process images with ThreadPool
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_image, image_paths)

    end_time = time.time()                        # end timer
    cpu_end, mem_end = get_resource_usage()       # CPU and memory usage at the end

    # calculate metrics based on difference
    thread_time = time.time() - start_time
    thread_throughput = len(image_paths) / thread_time
    thread_cpu = cpu_end - cpu_start
    thread_mem = mem_end - mem_start


    # ProcessPoolExecutor
    start_time = time.time()                      # start timer
    cpu_start, mem_start = get_resource_usage()   # CPU and memory usage at the start

    # process image with ProcessPool
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        executor.map(process_image, image_paths)

    end_time = time.time()                        # end timer
    cpu_end, mem_end = get_resource_usage()       # CPU and memory usage at the end

    # calculate metrics based on difference
    process_time = time.time() - start_time
    process_throughput = len(image_paths) / process_time
    process_cpu = cpu_end - cpu_start
    process_mem = mem_end - mem_start
    
    
    # display ThreadPoolExecutor metrics for user
    print(f"\nThreadPoolExecutor time: {thread_time:.4f} seconds")
    print(f"ThreadPoolExecutor throughput: {thread_throughput:.4f} images/sec")
    print(f"ThreadPoolExecutor CPU usage: {thread_cpu:.2f}%")
    print(f"ThreadPoolExecutor memory usage: {thread_mem:.2f} MB")

    # display ProcessPoolExecutor metrics for user
    print(f"\nProcessPoolExecutor time: {process_time:.4f} seconds")
    print(f"ProcessPoolExecutor throughput: {process_throughput:.4f} images/sec")
    print(f"ProcessPoolExecutor CPU usage: {process_cpu:.2f}%")
    print(f"ProcessPoolExecutor memory usage: {process_mem:.2f} MB")