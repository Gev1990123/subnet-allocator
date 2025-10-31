import ipaddress
import math
import argparse

def allocate_named_subnets(base_subnet, named_requirements):
    base_network = ipaddress.ip_network(base_subnet)
    available_subnets = [base_network]
    allocated_subnets = []

    for name, hosts in named_requirements:
        required_hosts = hosts + 2
        subnet_bits = math.ceil(math.log2(required_hosts))
        new_prefix = 32 - subnet_bits

        for i, net in enumerate(available_subnets):
            if net.prefixlen <= new_prefix:
                subnets = list(net.subnets(new_prefix=new_prefix))
                allocated_subnets.append((name, hosts, subnets[0]))
                available_subnets.pop(i)
                available_subnets.extend(subnets[1:])
                break
        else:
            raise ValueError(f"Not enough space for '{name}' ({hosts} hosts).")

    return allocated_subnets, sorted(available_subnets, key=lambda x: int(x.network_address))

def parse_named_subnets(subnet_str):
    named_list = []
    for item in subnet_str.split(","):
        name, count = item.split(":")
        named_list.append((name.strip(), int(count.strip())))
    return named_list

def main():
    parser = argparse.ArgumentParser(description="Allocate named subnets and show remaining space.")
    parser.add_argument("--base-subnet", required=True, help="Base subnet in CIDR notation")
    parser.add_argument("--subnets", required=True, help='Comma-separated list like "Wireless:500,Servers:200"')

    args = parser.parse_args()
    named_requirements = parse_named_subnets(args.subnets)

    try:
        allocated, remaining = allocate_named_subnets(args.base_subnet, named_requirements)

        print("\nAllocated Subnets:")
        print("-" * 40)
        for name, hosts, subnet in allocated:
            print(f"{name:<10} | Hosts: {hosts:<4} | Subnet: {subnet}")

        print("\nRemaining Unused Subnets:")
        print("-" * 40)
        for subnet in remaining:
            print(f"{subnet}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()