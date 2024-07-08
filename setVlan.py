#  python3 createVm.py --id 10000101 --vlan vlan10

import argparse
from functions import run_command, run_multiple_commands

parser = argparse.ArgumentParser(description='Connect to vm and update it using apt')
parser.add_argument('--id', required=True, help='VM ID')
parser.add_argument('--vlan', required=True, help='VLan name e.g. vmbr0 or vlan10')
args = parser.parse_args()

commands = [
  f"qm set {args.id} --net0 virtio,bridge={args.vlan}",
]

run_multiple_commands(commands)
