#pip install dnspython

import dns.resolver

def check_dns_propagation(domain, record_type='A', dns_servers=None):
    """
    Check the DNS propagation status for a domain and record type.

    Parameters:
    - domain: The domain to check.
    - record_type: The DNS record type (default is 'A').
    - dns_servers: List of DNS servers to query (default is None for a global check).

    Returns:
    - A dictionary where keys are DNS server names and values are the resolved IP addresses.
    """
    results = {}

    # Use the default resolver or specify custom DNS servers
    resolver = dns.resolver.Resolver()
    if dns_servers:
        resolver.nameservers = dns_servers

    try:
        answers = resolver.resolve(domain, record_type)
        results['Global'] = [str(answer) for answer in answers]
    except dns.resolver.NXDOMAIN:
        results['Global'] = 'NXDOMAIN (Not Found)'
    except dns.exception.DNSException as e:
        results['Global'] = f'Error: {e}'

    return results

def main():
    domain_to_check = 'google.com'
    record_type_to_check = 'A'

    #load dns servers from file
    with open('ns_list.txt') as f:
        custom_dns_servers = f.read().splitlines()
    # Specify a list of DNS servers from different locations
    #custom_dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222','208.67.222.220','103.86.99.100','12.121.117.201','9.9.9.9']

    for server in custom_dns_servers:
        server = [server]
        print(f'Checking {domain_to_check} ({server})')
        results = check_dns_propagation(domain_to_check, record_type_to_check, server)
        print(f"\033[96m{results['Global']}\033[00m")
        # Display results
        # for location, ips in results.items():
        #     print(f'\033[96m{location}: {ips}\033[00m')

if __name__ == "__main__":
    main()
