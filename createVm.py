#  python3 createVm.py --id 10000101 --name ethnode --cpu 4 --ram 4096 --disk 50G --os debian-12-generic-amd64-20240211 --ip 192.168.178.201 --gateway 192.168.178.1 --subnet 24 --pass HelloPass1

import argparse
import sys
from functions import run_command, run_multiple_commands

# Parse arguments
parser = argparse.ArgumentParser(description='Create and configure a Proxmox VM.')
parser.add_argument('--id', required=True, help='VM ID')
parser.add_argument('--name', required=True, help='VM Title')
parser.add_argument('--cpu', required=True, help='Number of CPU cores')
parser.add_argument('--ram', required=True, help='RAM size in MB')
parser.add_argument('--disk', required=True, help='Disk size, e.g., 25G')
parser.add_argument('--os', required=True, help='Operating System e.g. debian-12-generic-amd64-20240211')
parser.add_argument('--ip', required=True, help='IP address')
parser.add_argument('--subnet', required=True, help='Subnet, e.g., 24')
parser.add_argument('--gateway', required=True, help='Gateway IP address')
parser.add_argument('--pass', dest='password', required=True, help='Password for the VM')
args = parser.parse_args()

# Sanity check to ensure VM with the same ID does not already exist
exists, output = run_command(f"qm list | grep -qw {args.id}")
if exists:
    print(f"Error: VM with ID {args.id} already exists.")
    sys.exit(1)

exists, output = run_command(f"ping -qc 1 -W 2 {args.ip} 2>&1 | grep -qw '1 received'")
if exists:
    print(f"Error: IP {args.ip} is already in use.")
    sys.exit(1)

# Create and configure the VM
commands = [
    f"qm create {args.id} --name vm{args.name} --agent 1 --cpu host --cores {args.cpu} --memory {args.ram} --ciuser 'root' --cipassword '{args.password}' --net0 virtio,bridge=vmbr0 --ipconfig0 ip={args.ip}/{args.subnet},gw={args.gateway} --nameserver 8.8.4.4 --scsihw virtio-scsi-pci --machine q35",
    f"qm set {args.id} --scsi0 local-lvm:0,discard=on,ssd=1,format=qcow2,import-from=/var/lib/vz/htemplates/{args.os}.qcow2",
    f"qm disk resize {args.id} scsi0 {args.disk}",
    f"qm set {args.id} --boot order=scsi0",
    f"qm set {args.id} --bios ovmf --efidisk0 local:1,format=qcow2,efitype=4m,pre-enrolled-keys=1",
    f"qm set {args.id} --ide2 local:cloudinit",
    f"qm set {args.id} --sshkeys /root/.ssh/authorized_keys",
    f"qm start {args.id}",
]

run_multiple_commands(commands)

print(f"VM {args.id} created and configured successfully.")
