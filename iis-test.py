import requests
import time
import threading

# Target files to test
urls = [
    "https://example.com/static/a.js",
    "https://example.com/static/b.js"
]

# Timeout threshold in seconds to simulate a client disconnect
CLIENT_TIMEOUT = 5  # seconds

# Custom function to simulate a client timeout mid-transfer
def fetch_with_timeout(url, timeout=CLIENT_TIMEOUT):
    print(f"\nRequesting: {url}")
    start_time = time.time()
    try:
        with requests.get(url, stream=True, timeout=(3, None)) as r:
            total_bytes = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    total_bytes += len(chunk)
                if time.time() - start_time > timeout:
                    raise Exception("Simulated client disconnect (timeout exceeded)")
        duration = round((time.time() - start_time) * 1000, 2)
        print(f"Status: {r.status_code} | Bytes: {total_bytes} | Time Taken: {duration} ms")
    except Exception as e:
        duration = round((time.time() - start_time) * 1000, 2)
        print(f"Aborted: {e} | Time Taken: {duration} ms")

# Run for all target URLs
for url in urls:
    fetch_with_timeout(url)