import sys
import subprocess

# Function to run a command and return its output
def run_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        return True, output
    except subprocess.CalledProcessError as e:
        return False, e.output

def run_multiple_commands(commands):
  for cmd in commands:
    print(f"going to run {cmd}")
    success, output = run_command(cmd)
    if not success:
        print(f"Failed to execute command: {cmd}\nError: {output}")
        sys.exit(1)
