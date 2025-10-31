# Subnet Allocator CLI Tool

This Python CLI tool helps network engineers allocate subnets based on named host requirements from a given base subnet. It also displays remaining unused subnets.

## Features

- Allocate subnets with custom names (e.g., Wireless, Servers)
- Automatically calculates subnet sizes based on host counts
- Either output to a file named subnet_output.txt or display in CLI


## Usage

Print to CLI: 
```bash
python subnet_allocator.py --base-subnet 172.30.128.0/21 --subnets "Wireless:500,Servers:200,CCTV:50"
```

Export to File:
```bash
python subnet_allocator.py --base-subnet 172.30.128.0/21 --subnets "Wireless:500,Servers:200,CCTV:50" --export
```