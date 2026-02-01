
# Process Scheduling Module
# This file will contain the main scheduling logic and classes for Round-Robin and Priority-Based scheduling.

import heapq
import time
from collections import deque

class Process:
    def __init__(self, pid, burst_time, priority=0):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.arrival_time = 0  # For FCFS tie-breaker
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.response_time = None

    def __repr__(self):
        return f"Process(pid={self.pid}, burst={self.burst_time}, priority={self.priority})"

class Scheduler:
    def add_process(self, process):
        raise NotImplementedError
    def run(self):
        raise NotImplementedError

class RoundRobinScheduler(Scheduler):
    def __init__(self, time_slice=1):
        self.time_slice = time_slice
        self.queue = deque()
        self.current_time = 0
        self.finished = []

    def add_process(self, process):
        process.arrival_time = self.current_time
        self.queue.append(process)

    def run(self):
        print(f"Starting Round-Robin Scheduling with time slice = {self.time_slice}")
        while self.queue:
            process = self.queue.popleft()
            if process.start_time is None:
                process.start_time = self.current_time
                process.response_time = self.current_time - process.arrival_time
            run_time = min(self.time_slice, process.remaining_time)
            print(f"Running {process} for {run_time} unit(s)")
            time.sleep(run_time * 0.1)  # Simulate execution (scaled down)
            process.remaining_time -= run_time
            self.current_time += run_time
            if process.remaining_time > 0:
                self.queue.append(process)
            else:
                process.completion_time = self.current_time
                process.waiting_time = (process.completion_time - process.arrival_time - process.burst_time)
                print(f"Process {process.pid} completed at time {self.current_time}")
                self.finished.append(process)
        self.print_metrics()

    def print_metrics(self):
        print("\nPerformance Metrics (Round-Robin):")
        print("PID | Waiting | Turnaround | Response")
        for p in self.finished:
            turnaround = p.completion_time - p.arrival_time
            print(f"{p.pid:3} | {p.waiting_time:7} | {turnaround:10} | {p.response_time:8}")

class PriorityScheduler(Scheduler):
    def __init__(self):
        self.heap = []  # (priority, arrival_time, process)
        self.current_time = 0
        self.arrival_counter = 0
        self.finished = []

    def add_process(self, process):
        # Lower value = higher priority
        process.arrival_time = self.current_time
        heapq.heappush(self.heap, (process.priority, self.arrival_counter, process))
        self.arrival_counter += 1

    def run(self):
        print("Starting Priority-Based Scheduling")
        while self.heap:
            priority, arrival, process = heapq.heappop(self.heap)
            if process.start_time is None:
                process.start_time = self.current_time
                process.response_time = self.current_time - process.arrival_time
            print(f"Running {process} (priority={priority}) for {process.remaining_time} unit(s)")
            time.sleep(process.remaining_time * 0.1)  # Simulate execution (scaled down)
            self.current_time += process.remaining_time
            process.completion_time = self.current_time
            process.waiting_time = (process.completion_time - process.arrival_time - process.burst_time)
            process.remaining_time = 0
            print(f"Process {process.pid} completed at time {self.current_time}")
            self.finished.append(process)
        self.print_metrics()

    def print_metrics(self):
        print("\nPerformance Metrics (Priority-Based):")
        print("PID | Waiting | Turnaround | Response")
        for p in self.finished:
            turnaround = p.completion_time - p.arrival_time
            print(f"{p.pid:3} | {p.waiting_time:7} | {turnaround:10} | {p.response_time:8}")
