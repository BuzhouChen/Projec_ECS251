import concurrent.futures
import requests
import time

URLS = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.baidu.com"
] * 50  # 请求次数增加到200次

def fetch_url(url):
    try:
        # 使用 requests 进行网络请求，并设置超时参数
        response = requests.get(url, timeout=10)  # 设置请求的超时为 10 秒
        response.raise_for_status()  # 如果响应状态码不是 2xx，会抛出异常
        return f"{url}: {response.status_code}"
    except requests.Timeout:
        return f"{url}: Timeout error"
    except requests.ConnectionError:
        return f"{url}: Connection error"
    except requests.RequestException as e:
        return f"{url}: Error - {str(e)}"


if __name__ == "__main__":
    # 使用 ThreadPoolExecutor
    print("Using ThreadPoolExecutor...")
    start = time.time()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results_threadpool = list(executor.map(fetch_url, URLS))
    except Exception as e:
        print(f"Error in ThreadPoolExecutor: {e}")
    end = time.time()
    print(f"ThreadPool - Time taken: {end - start:.2f}s")

    # # 打印 ThreadPoolExecutor 的结果
    # for result in results_threadpool:
    #     print(result)

    # 使用 ProcessPoolExecutor
    print("\nUsing ProcessPoolExecutor...")
    start = time.time()
    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            results_processpool = list(executor.map(fetch_url, URLS))
    except Exception as e:
        print(f"Error in ProcessPoolExecutor: {e}")
    end = time.time()
    print(f"ProcessPool - Time taken: {end - start:.2f}s")

    # # 打印 ProcessPoolExecutor 的结果
    # for result in results_processpool:
    #     print(result)
    
    
# Using ThreadPoolExecutor...
# ThreadPool - Time taken: 7.47s

# Using ProcessPoolExecutor...
# ProcessPool - Time taken: 7.60s