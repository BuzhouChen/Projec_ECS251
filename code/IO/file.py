import os
import concurrent.futures
import time

def generate_large_file(filename, size_in_mb=50):
    """generate files"""
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_in_mb * 1024 * 1024))

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    
    file_list = [f"./data/big_file_{i}.txt" for i in range(10)]
    out_file_list = [f"./data/output_{i}.txt" for i in range(len(file_list))]
    
    # record the time of start
    start_time = time.time()
    for fname in file_list:
        generate_large_file(fname, size_in_mb=100)  # generate a 100 MB file
    end_time = time.time()
    print(f"File generation time: {end_time - start_time:.2f} seconds")
    
    
    # Read files using ThreadPoolExecutor
    start_time = time.time()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            contents_threadpool = list(executor.map(read_file, file_list))
    except Exception as e:
        print(f"Error in ThreadPoolExecutor (reading files): {e}")
    end_time = time.time()
    print(f"File reading time (ThreadPool): {end_time - start_time:.2f} seconds")
    
    # Read files using ProcessPoolExecutor
    start_time = time.time()
    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            contents_processpool = list(executor.map(read_file, file_list))
    except Exception as e:
        print(f"Error in ProcessPoolExecutor (reading files): {e}")
    end_time = time.time()
    print(f"File reading time (ProcessPool): {end_time - start_time:.2f} seconds")
    
    # Write files using ThreadPoolExecutor
    start_time = time.time()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(write_file, contents_threadpool, out_file_list)
    except Exception as e:
        print(f"Error in ThreadPoolExecutor (writing files): {e}")
    end_time = time.time()
    print(f"File writing time (ThreadPool): {end_time - start_time:.2f} seconds")
    
    # Write files using ProcessPoolExecutor
    start_time = time.time()
    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            executor.map(write_file, contents_processpool, out_file_list)
    except Exception as e:
        print(f"Error in ProcessPoolExecutor (writing files): {e}")
    end_time = time.time()
    print(f"File writing time (ProcessPool): {end_time - start_time:.2f} seconds")
    

# File generation time: 1.49 seconds
# File reading time (ThreadPool): 0.42 seconds
# File reading time (ProcessPool): 2.51 seconds
# File writing time (ThreadPool): 0.36 seconds
# File writing time (ProcessPool): 2.10 seconds