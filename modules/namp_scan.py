import nmap
from config import NMAP_ARGUMENTS

def scan_network(target):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target, arguments=NMAP_ARGUMENTS)
        results = []
        for host in nm.all_hosts():
            host_info = {
                'host': host,
                'hostname': nm[host].hostname(),
                'state': nm[host].state(),
                'services': []
            }
            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    service_info = {
                        'port': port,
                        'name': nm[host][proto][port]['name'],
                        'state': nm[host][proto][port]['state'],
                        'product': nm[host][proto][port]['product'],
                        'version': nm[host][proto][port]['version'],
                        'extrainfo': nm[host][proto][port]['extrainfo'],
                        'cpe': nm[host][proto][port].get('cpe')
                    }
                    host_info['services'].append(service_info)
            results.append(host_info)
        return results
    except nmap.PortScannerError as e:
        raise RuntimeError(f"Error scanning network: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")
