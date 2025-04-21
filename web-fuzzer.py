import requests
import threading
import argparse
import time
from queue import Queue
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

parser = argparse.ArgumentParser(description="Web Fuzzer", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--url", required=True, help="URL --> example: http(s)://hostname:port, if you are using a port other than 80 or 443")
parser.add_argument("-w", "--wordlist", required=True, help="HTML Tag --> example: /path/to/wordlist.txt")
parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use")
parser.add_argument("-e", "--extension", default="", help="File extension to append to each word in the wordlist (e.g., .php, .html). Only one extension")
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6788.76 Safari/537.36"

def check_url(url):
    path = url.split("://")[1].split("/")[1]
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": user_agent}, verify=False)
        return response.status_code, path
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def fuzzer(queue, url, lock, progress, total_words):

    while not queue.empty():
        word = queue.get()
        full_url = f"{url}/{word}"
        try:
            with lock:
                progress[0] += 1
                response_code, path = check_url(full_url)
                if response_code != 404:
                    print(f"Found: /{path} - Status Code: {response_code}")
        except Exception as e:
            print(f"Error: {e}")

def show_progress(progress, total_words):
    while True:
        input()
        print(f"Progress: {progress[0]}/{total_words}")

def run_scanner(url, wordlist, threads, extension=None):
    queue = Queue()
    lock = threading.Lock()
    progress = [0]

    thread_list = []
    with open(wordlist, "r") as file:
        words = file.readlines()
        total_words = 0
        if extension:
            for line in words:
                if line[0] != "#":
                    queue.put(line.strip() + extension)
                    total_words += 1
        else:
            for line in words:
                if line[0] != "#":
                    queue.put(line.strip())
                    total_words += 1

    progress_thread = threading.Thread(target=show_progress, args=(progress, total_words), daemon=True)
    progress_thread.start()

    for t in range(threads):
        thread = threading.Thread(target=fuzzer, kwargs={"queue": queue, "url": url, "lock": lock, "progress": progress, "total_words": total_words}) 
        thread.daemon = True
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    queue.join()

    for thread in thread_list:
        thread.join()

    print("Fuzz completed!")

if __name__ == "__main__":
    args = parser.parse_args()
    url = args.url
    wordlist = args.wordlist
    threads = args.threads
    extension = args.extension
    
    print("Starting Web Fuzzer...")
    print(f"Fuzzing URL: {url}")
    print(f"Wordlist: {wordlist}")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    print("Press any key to show progress...")
    print("-" * 64)
    run_scanner(url, wordlist, threads, extension)
    