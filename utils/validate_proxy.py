import requests
import threading
import queue

NUM_THREADS = 10
proxy_file_path = ""
output_file_path = ""

q = queue.Queue()
valid_proxies = []


def check_proxies():
    global q, valid_proxies
    while True:
        proxy = q.get()
        if proxy is None:
            break
        try:
            res = requests.get(
                "http://ipinfo.io/json",
                proxies={"http": proxy, "https": proxy},
                timeout=5,
            )
            if res.status_code == 200:
                print(proxy)
                valid_proxies.append(proxy)
        except requests.RequestException:
            pass
        finally:
            q.task_done()


# Read proxies from file and enqueue them
with open(proxy_file_path, "r") as f:
    for line in f:
        q.put(line.strip())

# Create threads
threads = []
for _ in range(NUM_THREADS):
    thread = threading.Thread(target=check_proxies)
    threads.append(thread)
    thread.start()

# Wait for all tasks to be processed
q.join()

# Signal threads to exit
for _ in range(NUM_THREADS):
    q.put(None)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Write valid proxies to a file
with open(output_file_path, "w") as output_file:
    output_file.write("\n".join(valid_proxies))
