


# --- Required Imports ---
import os
import shlex
import subprocess
from auth import authenticate, check_permission, USERS
import sys



# --- User Authentication ---
def login():
	print("Welcome to the Secure Shell!")
	for _ in range(3):
		username = input("Username: ")
		password = input("Password: ")
		user = authenticate(username, password)
		if user:
			print(f"Login successful. Welcome, {username} ({user['role']})!")
			return username, user
		else:
			print("Invalid credentials. Try again.")
	print("Too many failed attempts. Exiting.")
	exit(1)

# --- File Permission Wrapper ---
def permissioned_open(user, filename, mode):
	mode_char = mode[0]
	if not check_permission(user, filename, mode_char):
		raise PermissionError(f"Access denied: {mode_char} permission required for {filename}")
	return open(filename, mode)

# --- Command Execution with Piping ---
def execute_piped_commands(commands, user):
	processes = []
	prev_stdout = None
	for i, cmd in enumerate(commands):
		args = shlex.split(cmd)
		# Permission check for file commands (simulate for 'cat', 'less', 'more', 'head', 'tail')
		if args and args[0] in ("cat", "less", "more", "head", "tail") and len(args) > 1:
			for fname in args[1:]:
				try:
					permissioned_open(user, fname, 'r').close()
				except Exception as e:
					print(e)
					return
		proc = subprocess.Popen(args, stdin=prev_stdout, stdout=subprocess.PIPE if i < len(commands)-1 else None)
		if prev_stdout:
			prev_stdout.close()
		prev_stdout = proc.stdout
		processes.append(proc)
	# Wait for last process
	if processes:
		processes[-1].wait()

# --- Main Shell Loop ---
def main():
	username, user = login()
	def show_menu():
		print("\n==== Integration Menu ====")
		print("1. Basic Shell (Deliverable 1)")
		print("2. Scheduling Demo (Deliverable 2)")
		print("3. Memory Management Demo (Deliverable 3)")
		print("4. Synchronization Demo (Deliverable 3)")
		print("5. Return to main shell")
		return input("Select an option: ")

	while True:
		try:
			cmdline = input(f"{username}@shell$ ")
			if cmdline.strip() in ("exit", "quit"):
				print("Goodbye!")
				break
			if cmdline.strip() == "menu":
				while True:
					choice = show_menu()
					if choice == '1':
						# Run basic shell from Deliverable 1
						shell1_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Project_Deliverable1/shell.py'))
						print("Launching basic shell. Type 'exit' to return.")
						os.system(f'python3 "{shell1_path}"')
					elif choice == '2':
						# Run scheduling demo from Deliverable 2
						sched_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Project_Deliverable2/shell_sched.py'))
						if os.path.exists(sched_path):
							print("Launching scheduling demo. Type 'exit' to return.")
							os.system(f'python3 "{sched_path}"')
						else:
							print("Scheduling demo not found.")
					elif choice == '3':
						# Run memory management demo from Deliverable 3
						mem_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Project_Deliverable3/shell_mem_sync.py'))
						if os.path.exists(mem_path):
							print("Launching memory management demo. Type '3' in the menu to exit.")
							os.system(f'python3 "{mem_path}"')
						else:
							print("Memory management demo not found.")
					elif choice == '4':
						# Run synchronization demo from Deliverable 3 (same as memory for this shell)
						mem_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Project_Deliverable3/shell_mem_sync.py'))
						if os.path.exists(mem_path):
							print("Launching synchronization demo. Type '3' in the menu to exit.")
							os.system(f'python3 "{mem_path}"')
						else:
							print("Synchronization demo not found.")
					elif choice == '5':
						break
					else:
						print("Invalid option. Try again.")
				continue
			if '|' in cmdline:
				commands = [c.strip() for c in cmdline.split('|')]
				execute_piped_commands(commands, user)
			else:
				args = shlex.split(cmdline)
				if not args:
					continue
				# Permission check for file commands
				if args[0] in ("cat", "less", "more", "head", "tail") and len(args) > 1:
					for fname in args[1:]:
						try:
							permissioned_open(user, fname, 'r').close()
						except Exception as e:
							print(e)
							break
					else:
						subprocess.run(args)
				else:
					subprocess.run(args)
		except PermissionError as e:
			print(e)
		except Exception as e:
			print(f"Error: {e}")

if __name__ == "__main__":
	main()
