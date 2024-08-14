import subprocess
import shlex
import logging

logger = logging.getLogger(__name__)

def gather_info(target: str) -> dict:
    """Gather WHOIS, DNS, and traceroute information for the given target."""
    results = {}
    try:
        whois_result = subprocess.run(shlex.split(f'whois {target}'), capture_output=True, text=True, check=True, timeout=120).stdout
        dns_result = subprocess.run(shlex.split(f'nslookup {target}'), capture_output=True, text=True, check=True, timeout=60).stdout
        traceroute_result = subprocess.run(shlex.split(f'traceroute {target}'), capture_output=True, text=True, check=True, timeout=180).stdout

        results['whois'] = whois_result
        results['dns'] = dns_result
        results['traceroute'] = traceroute_result

        logger.info(f"Information gathering completed for target {target}.")
        return results
    except subprocess.CalledProcessError as e:
        logger.error(f"Error gathering information: {e}")
        return {"error": f"Error gathering information: {e.output}"}
    except subprocess.TimeoutExpired:
        logger.error(f"Information gathering timed out for target {target}.")
        return {"error": "Information gathering timed out."}
    except Exception as e:
        logger.error(f"Unexpected error during information gathering for {target}: {e}")
        return {"error": f"Unexpected error: {e}"}
