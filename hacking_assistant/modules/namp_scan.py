import nmap
import logging
from config import NMAP_ARGUMENTS

logger = logging.getLogger(__name__)

def scan_network(target: str) -> list:
    """Scan the network for open ports and services using nmap."""
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
        logger.info(f"Network scan completed for target {target}.")
        return results
    except nmap.PortScannerError as e:
        logger.error(f"Error scanning network: {e}")
        raise RuntimeError(f"Error scanning network: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during network scan for target {target}: {e}")
        raise RuntimeError(f"Unexpected error: {e}")
