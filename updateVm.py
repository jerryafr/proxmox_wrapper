#  python3 updateVm.py --ip 192.168.178.201

import argparse
from functions import run_command, run_multiple_commands

parser = argparse.ArgumentParser(description='Connect to vm and update it using apt')
parser.add_argument('--ip', required=True, help='IP address')
args = parser.parse_args()

commands = [
  f"while ! ping -c1 {args.ip}; do sleep 1; done; echo 'done'",
  f"while ! nc -zv {args.ip} 22; do sleep 1; done; echo 'done'",
  f"sleep 10; ssh -o StrictHostKeyChecking=no root@{args.ip} 'apt update && apt upgrade -y'"
]

run_multiple_commands(commands)
