#!/usr/bin/env python3
"""
Advanced Shell Simulation - Deliverable 1: Basic Shell Implementation and Process Management

Features:
- Accepts and executes user commands
- Implements built-in commands: cd, pwd, exit, echo, clear, ls, cat, mkdir, rmdir, rm, touch, kill
- Supports foreground (&) and background execution
- Tracks running processes and provides job control: jobs, fg, bg
- Handles errors for invalid commands and inputs

Run: python3 shell.py
"""
import os
import sys
import shlex
import subprocess
import signal

JOBS = []  # List of background jobs: dicts with keys: id, pid, cmd, status
JOB_ID = 1

# Built-in command implementations
def cmd_cd(args):
    try:
        os.chdir(args[1] if len(args) > 1 else os.path.expanduser('~'))
    except Exception as e:
        print(f"cd: {e}")

def cmd_pwd(args):
    print(os.getcwd())

def cmd_exit(args):
    print("Exiting shell.")
    sys.exit(0)

def cmd_echo(args):
    print(' '.join(args[1:]))

def cmd_clear(args):
    os.system('clear')

def cmd_ls(args):
    for f in os.listdir(os.getcwd()):
        print(f)

def cmd_cat(args):
    if len(args) < 2:
        print("cat: missing filename")
        return
    try:
        with open(args[1], 'r') as f:
            print(f.read(), end='')
    except Exception as e:
        print(f"cat: {e}")

def cmd_mkdir(args):
    if len(args) < 2:
        print("mkdir: missing directory name")
        return
    try:
        os.mkdir(args[1])
    except Exception as e:
        print(f"mkdir: {e}")

def cmd_rmdir(args):
    if len(args) < 2:
        print("rmdir: missing directory name")
        return
    try:
        os.rmdir(args[1])
    except Exception as e:
        print(f"rmdir: {e}")

def cmd_rm(args):
    if len(args) < 2:
        print("rm: missing filename")
        return
    try:
        os.remove(args[1])
    except Exception as e:
        print(f"rm: {e}")

def cmd_touch(args):
    if len(args) < 2:
        print("touch: missing filename")
        return
    try:
        with open(args[1], 'a'):
            os.utime(args[1], None)
    except Exception as e:
        print(f"touch: {e}")

def cmd_kill(args):
    if len(args) < 2:
        print("kill: missing pid")
        return
    try:
        os.kill(int(args[1]), signal.SIGTERM)
    except Exception as e:
        print(f"kill: {e}")

def cmd_jobs(args):
    for job in JOBS:
        print(f"[{job['id']}] {job['pid']} {job['status']} {job['cmd']}")

def cmd_fg(args):
    if len(args) < 2:
        print("fg: missing job id")
        return
    try:
        job_id = int(args[1])
        for job in JOBS:
            if job['id'] == job_id:
                os.waitpid(job['pid'], 0)
                job['status'] = 'Done'
                print(f"Brought job [{job_id}] to foreground.")
                return
        print(f"fg: job {job_id} not found")
    except Exception as e:
        print(f"fg: {e}")

def cmd_bg(args):
    if len(args) < 2:
        print("bg: missing job id")
        return
    try:
        job_id = int(args[1])
        for job in JOBS:
            if job['id'] == job_id:
                os.kill(job['pid'], signal.SIGCONT)
                job['status'] = 'Running'
                print(f"Resumed job [{job_id}] in background.")
                return
        print(f"bg: job {job_id} not found")
    except Exception as e:
        print(f"bg: {e}")

BUILTINS = {
    'cd': cmd_cd,
    'pwd': cmd_pwd,
    'exit': cmd_exit,
    'echo': cmd_echo,
    'clear': cmd_clear,
    'ls': cmd_ls,
    'cat': cmd_cat,
    'mkdir': cmd_mkdir,
    'rmdir': cmd_rmdir,
    'rm': cmd_rm,
    'touch': cmd_touch,
    'kill': cmd_kill,
    'jobs': cmd_jobs,
    'fg': cmd_fg,
    'bg': cmd_bg,
}

def run_command(cmdline):
    global JOB_ID
    if not cmdline.strip():
        return
    args = shlex.split(cmdline)
    if not args:
        return
    background = False
    if args[-1] == '&':
        background = True
        args = args[:-1]
    if args[0] in BUILTINS:
        BUILTINS[args[0]](args)
        return
    try:
        proc = subprocess.Popen(args)
        if background:
            JOBS.append({'id': JOB_ID, 'pid': proc.pid, 'cmd': cmdline, 'status': 'Running'})
            print(f"Started job [{JOB_ID}] {proc.pid} in background.")
            JOB_ID += 1
        else:
            proc.wait()
    except FileNotFoundError:
        print(f"{args[0]}: command not found")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Welcome to Advanced Shell Simulation! Type 'exit' to quit.")
    while True:
        try:
            cmdline = input(f"{os.getcwd()}$ ")
            run_command(cmdline)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

if __name__ == "__main__":
    main()
