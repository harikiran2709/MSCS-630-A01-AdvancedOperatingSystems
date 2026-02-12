import threading
import time
import random
from collections import deque

# ---------------------- Memory Management (Paging) ----------------------

class Page:
    def __init__(self, process_id, page_number):
        self.process_id = process_id
        self.page_number = page_number
        self.last_used = time.time()

    def __repr__(self):
        return f"P{self.process_id}:Pg{self.page_number}"

class MemoryManager:
    def __init__(self, num_frames, replacement_algo='FIFO'):
        self.num_frames = num_frames
        self.frames = []  # List of Page objects
        self.page_faults = 0
        self.replacement_algo = replacement_algo
        self.fifo_queue = deque()
        self.lru_dict = {}

    def request_page(self, process_id, page_number):
        # Check if page is already in memory
        for page in self.frames:
            if page.process_id == process_id and page.page_number == page_number:
                if self.replacement_algo == 'LRU':
                    page.last_used = time.time()
                print(f"Page {page} already in memory.")
                return False  # No page fault
        # Page fault
        self.page_faults += 1
        print(f"Page fault: loading {process_id}:{page_number}")
        new_page = Page(process_id, page_number)
        if len(self.frames) < self.num_frames:
            self.frames.append(new_page)
            if self.replacement_algo == 'FIFO':
                self.fifo_queue.append(new_page)
        else:
            self.replace_page(new_page)
        return True  # Page fault occurred

    def replace_page(self, new_page):
        if self.replacement_algo == 'FIFO':
            old_page = self.fifo_queue.popleft()
            idx = self.frames.index(old_page)
            print(f"[FIFO] Replacing {old_page} with {new_page}")
            self.frames[idx] = new_page
            self.fifo_queue.append(new_page)
        elif self.replacement_algo == 'LRU':
            # Find least recently used
            lru_page = min(self.frames, key=lambda p: p.last_used)
            idx = self.frames.index(lru_page)
            print(f"[LRU] Replacing {lru_page} with {new_page}")
            self.frames[idx] = new_page
        else:
            raise ValueError("Unknown replacement algorithm")

    def show_memory(self):
        print(f"Current memory frames: {self.frames}")

    def reset(self):
        self.frames = []
        self.page_faults = 0
        self.fifo_queue = deque()

# ---------------------- Process Synchronization (Producer-Consumer) ----------------------

class ProducerConsumer:
    def __init__(self, buffer_size=5):
        self.buffer = deque(maxlen=buffer_size)
        self.buffer_size = buffer_size
        self.mutex = threading.Lock()
        self.empty = threading.Semaphore(buffer_size)
        self.full = threading.Semaphore(0)
        self.running = True

    def producer(self, pid):
        while self.running:
            item = random.randint(1, 100)
            self.empty.acquire()
            with self.mutex:
                self.buffer.append(item)
                print(f"Producer {pid} produced {item}. Buffer: {list(self.buffer)}")
            self.full.release()
            time.sleep(random.uniform(0.2, 0.7))

    def consumer(self, pid):
        while self.running:
            self.full.acquire()
            with self.mutex:
                item = self.buffer.popleft()
                print(f"Consumer {pid} consumed {item}. Buffer: {list(self.buffer)}")
            self.empty.release()
            time.sleep(random.uniform(0.2, 0.7))

    def start(self, num_producers=1, num_consumers=1, duration=5):
        threads = []
        self.running = True
        for i in range(num_producers):
            t = threading.Thread(target=self.producer, args=(i+1,))
            t.start()
            threads.append(t)
        for i in range(num_consumers):
            t = threading.Thread(target=self.consumer, args=(i+1,))
            t.start()
            threads.append(t)
        time.sleep(duration)
        self.running = False
        # Unblock any waiting threads
        for _ in range(self.buffer_size):
            self.empty.release()
            self.full.release()
        for t in threads:
            t.join()
        print("Producer-Consumer simulation complete.")

# ---------------------- Shell Interface ----------------------

def memory_management_demo():
    print("\n--- Memory Management Demo ---")
    num_frames = int(input("Enter number of memory frames: "))
    algo = input("Choose page replacement algorithm (FIFO/LRU): ").strip().upper()
    mm = MemoryManager(num_frames, algo)
    num_processes = int(input("Enter number of processes: "))
    for pid in range(1, num_processes+1):
        pages = input(f"Enter page requests for process {pid} (space-separated): ").split()
        for page in pages:
            mm.request_page(pid, int(page))
            mm.show_memory()
    print(f"Total page faults: {mm.page_faults}")
    mm.show_memory()
    print("--- End of Memory Management Demo ---\n")

def producer_consumer_demo():
    print("\n--- Producer-Consumer Synchronization Demo ---")
    buffer_size = int(input("Enter buffer size: "))
    num_producers = int(input("Number of producers: "))
    num_consumers = int(input("Number of consumers: "))
    duration = int(input("Simulation duration (seconds): "))
    pc = ProducerConsumer(buffer_size)
    pc.start(num_producers, num_consumers, duration)
    print("--- End of Producer-Consumer Demo ---\n")

def main():
    while True:
        print("\n==== Shell Menu ====")
        print("1. Memory Management (Paging)")
        print("2. Process Synchronization (Producer-Consumer)")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            memory_management_demo()
        elif choice == '2':
            producer_consumer_demo()
        elif choice == '3':
            print("Exiting shell.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
