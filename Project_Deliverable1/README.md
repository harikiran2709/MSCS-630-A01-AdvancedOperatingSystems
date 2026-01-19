
# Advanced Shell Simulation - Deliverable 1 Report

## Code Submission
The complete source code for the shell, including all built-in commands and process management, is provided in `shell.py` in this directory.

## Screenshots (Instructions)
To include screenshots in your submission:
- Show execution of built-in commands (e.g., `pwd`, `ls`, `echo`, `mkdir`, `cat`, etc.).
- Demonstrate foreground and background process management:
	- Start a background job (e.g., `sleep 10 &`).
	- Use `jobs` to list background jobs.
	- Use `fg` and `bg` to manage jobs.
- Show error handling for invalid commands (e.g., `rm missingfile`, `unknowncmd`, `fg 99`).

## Process Management
When a user enters a command, the shell checks if it is a built-in command. If so, it is executed directly in the shell process. For external commands, the shell uses Python's `subprocess.Popen` to create a new process. If the command ends with `&`, it is run in the background and tracked in a job list with its process ID and status. Foreground processes are waited on by the shell until completion. The shell supports job control commands (`jobs`, `fg`, `bg`) to manage background jobs.

## Error Handling
The shell checks for missing arguments, invalid commands, and file/directory errors. For example, if a required argument is missing (e.g., `cat` without a filename), the shell prints a helpful error message. If a command is not found, it reports '`command not found`'. Invalid job IDs for `fg`/`bg` are also handled with clear feedback.

## Challenges and Improvements
One challenge was simulating job control and process management in Python, which is less direct than in C/C++. The shell uses a job list and basic signal handling to track and manage background jobs. Another challenge was ensuring robust error handling for all built-in commands and user inputs. Future improvements could include more advanced signal management, support for pipelines, and I/O redirection.

## Example Usage
```
pwd
ls
echo Hello World
mkdir testdir
touch testfile
cat testfile
sleep 10 &
jobs
fg 1
rm missingfile
unknowncmd
```

See `shell.py` for the full implementation.
