#  python3 setVlan.py --id 10000101 --vlan vlan10 --tag 10

import argparse
from functions import run_command, run_multiple_commands

parser = argparse.ArgumentParser(description='Connect to vm and update it using apt')
parser.add_argument('--id', required=True, help='VM ID')
parser.add_argument('--bridge', required=True, help='Bridge name e.g. vmbr0')
parser.add_argument('--tag', required=True, help='VLan tag e.g. 10')
args = parser.parse_args()

commands = [
  f"qm set {args.id} --net0 virtio,bridge={args.bridge},tag={args.tag}",
]

run_multiple_commands(commands)
