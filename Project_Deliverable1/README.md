
# Advanced Shell Simulation - Deliverable 1 Report

## Code Submission
The complete source code for the shell, including all built-in commands and process management, is provided in `shell.py` in this directory.

## Features:
- Accepts and executes user commands
- Implements built-in commands: cd, pwd, exit, echo, clear, ls, cat, mkdir, rmdir, rm, touch, kill
- Supports foreground (&) and background execution
- Tracks running processes and provides job control: jobs, fg, bg
- Handles errors for invalid commands and inputs

run python3 shell.py

## Example Usage
```
Built-in commands
mkdir testdir
cd testdir
pwd
cd ..
pwd
ls
echo Hello World
mkdir testdir
ls
rmdir testdir
ls
touch testfile
nano testfile
cat testfile
sleep 30 &
jobs
kill <pid>

Process Management and Job Control
a. Foreground Execution
sleep 10

b. Background Execution
sleep 10 &
jobs

c. Bring Job to Foreground
fg 1

d. Resume Job in Background
sleep 30 &
kill -STOP <pid>
jobs
bg 2


Error Handling
a. Invalid Command
notacommand

b. Missing Arguments
cat

c. Invalid Job ID
fg 99
```
