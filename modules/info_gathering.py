import subprocess

def gather_info(target):
    try:
        whois_result = subprocess.run(['whois', target], capture_output=True, text=True).stdout
        dns_result = subprocess.run(['nslookup', target], capture_output=True, text=True).stdout
        traceroute_result = subprocess.run(['traceroute', target], capture_output=True, text=True).stdout
        combined_result = f"WHOIS Information:\n{whois_result}\n\nDNS Information:\n{dns_result}\n\nTraceroute Information:\n{traceroute_result}"
        return combined_result
    except subprocess.CalledProcessError as e:
        return f"Error gathering information: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
