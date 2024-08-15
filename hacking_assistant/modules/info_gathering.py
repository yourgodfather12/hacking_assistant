import subprocess
import shlex
import logging

logger = logging.getLogger(__name__)

def gather_info(target: str) -> dict:
    """
    Gather WHOIS, DNS, and traceroute information for the given target.
    :param target: The target IP or hostname.
    :return: A dictionary containing gathered information.
    """
    results = {}
    try:
        whois_result = subprocess.run(shlex.split(f'whois {target}'), capture_output=True, text=True, check=True, timeout=120).stdout
        dns_result = subprocess.run(shlex.split(f'nslookup {target}'), capture_output=True, text=True, check=True, timeout=60).stdout
        traceroute_result = subprocess.run(shlex.split(f'traceroute {target}'), capture_output=True, text=True, check=True, timeout=180).stdout

        results['whois'] = whois_result if whois_result else "No WHOIS data found."
        results['dns'] = dns_result if dns_result else "No DNS data found."
        results['traceroute'] = traceroute_result if traceroute_result else "No Traceroute data found."

        logger.info(f"Information gathering completed for target {target}.")
        return results
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed during information gathering for {target}: {e}")
        return {"error": f"An error occurred: {e.output}"}
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out during information gathering for {target}.")
        return {"error": "Error: Command timed out."}
    except Exception as e:
        logger.error(f"Unexpected error during information gathering of {target}: {e}")
        return {"error": f"Unexpected error: {e}"}
