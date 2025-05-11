import requests
import time
import threading
import argparse

# Target URLs
urls = [
    "https://example.com/static/a.js",
    "https://example.com/static/b.js"
]

# Custom headers
headers = {
    "User-Agent": "latency-test"
}

# ANSI escape codes for colored output
RED = "\033[91m"
RESET = "\033[0m"

# Request function
def fetch_with_timeout(url, duration, timeout):
    end_time = time.time() + duration
    while time.time() < end_time:
        start = time.time()
        try:
            with requests.get(url, stream=True, timeout=(3, None), headers=headers) as r:
                total_bytes = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        total_bytes += len(chunk)
                    if time.time() - start > timeout:
                        raise Exception("Simulated client disconnect")
            elapsed = round((time.time() - start) * 1000, 2)
            output = f"[{url}] 200 OK | {total_bytes} bytes | Time: {elapsed} ms"
        except Exception as e:
            elapsed = round((time.time() - start) * 1000, 2)
            output = f"[{url}] Aborted: {str(e)} | Time: {elapsed} ms"

        # Highlight slow requests
        if elapsed > 5000:
            print(RED + output + RESET)
        else:
            print(output)

# Worker for each thread
def worker(duration, timeout):
    for url in urls:
        fetch_with_timeout(url, duration, timeout)

# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate high-latency static file requests.")
    parser.add_argument("--threads", type=int, default=4, help="Number of concurrent threads")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("--client_timeout", type=int, default=5, help="Client-side abort timeout (seconds)")
    args = parser.parse_args()

    thread_list = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(args.duration, args.client_timeout))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()