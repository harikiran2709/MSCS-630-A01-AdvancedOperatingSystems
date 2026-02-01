# Shell interface for process scheduling simulation
# Allows user to select scheduling algorithm, add processes, and start simulation

from scheduler import Process, RoundRobinScheduler, PriorityScheduler

# Placeholder for shell logic


def main():
    print("Welcome to the Process Scheduling Shell!")
    scheduler = None
    time_slice = 1
    pid_counter = 1
    while True:
        print("\nMenu:")
        print("1. Select Scheduling Algorithm")
        print("2. Set Time Slice (Round-Robin)")
        print("3. Add Process")
        print("4. Start Scheduling Simulation")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            print("a. Round-Robin Scheduling")
            print("b. Priority-Based Scheduling")
            algo = input("Select algorithm (a/b): ")
            if algo == 'a':
                scheduler = RoundRobinScheduler(time_slice)
                print("Round-Robin selected.")
            elif algo == 'b':
                scheduler = PriorityScheduler()
                print("Priority-Based selected.")
            else:
                print("Invalid selection.")
        elif choice == '2':
            ts = input("Enter time slice (integer): ")
            try:
                time_slice = int(ts)
                print(f"Time slice set to {time_slice}.")
                if isinstance(scheduler, RoundRobinScheduler):
                    scheduler.time_slice = time_slice
            except ValueError:
                print("Invalid time slice.")
        elif choice == '3':
            burst = input("Enter burst time (integer): ")
            try:
                burst = int(burst)
            except ValueError:
                print("Invalid burst time.")
                continue
            if isinstance(scheduler, PriorityScheduler):
                prio = input("Enter priority (lower number = higher priority): ")
                try:
                    prio = int(prio)
                except ValueError:
                    print("Invalid priority.")
                    continue
                proc = Process(pid_counter, burst, prio)
            else:
                proc = Process(pid_counter, burst)
            scheduler.add_process(proc)
            print(f"Process {pid_counter} added.")
            pid_counter += 1
        elif choice == '4':
            if scheduler is None:
                print("Select a scheduling algorithm first.")
            else:
                scheduler.run()
        elif choice == '5':
            print("Exiting shell.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
