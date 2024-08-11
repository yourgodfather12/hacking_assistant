import subprocess
import shlex
import logging

logger = logging.getLogger(__name__)

def gather_info(target):
    try:
        whois_result = subprocess.run(shlex.split(f'whois {target}'), capture_output=True, text=True, check=True).stdout
        dns_result = subprocess.run(shlex.split(f'nslookup {target}'), capture_output=True, text=True, check=True).stdout
        traceroute_result = subprocess.run(shlex.split(f'traceroute {target}'), capture_output=True, text=True, check=True).stdout
        combined_result = f"WHOIS Information:\n{whois_result}\n\nDNS Information:\n{dns_result}\n\nTraceroute Information:\n{traceroute_result}"
        return combined_result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error gathering information: {e}")
        return f"Error gathering information: {e.output}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"
