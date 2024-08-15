import requests
import logging

logger = logging.getLogger(__name__)

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/1.0"

def fetch_cve(cve_id: str) -> dict:
    """
    Fetch CVE details from the NVD API.
    :param cve_id: The CVE ID (e.g., "CVE-2023-0001").
    :return: A dictionary containing CVE details or an error message.
    """
    try:
        response = requests.get(f"{NVD_API_URL}?cveId={cve_id}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        cve_data = response.json()
        if cve_data['totalResults'] == 0:
            logger.warning(f"No data found for CVE ID: {cve_id}")
            return {"error": f"No data found for CVE ID: {cve_id}"}
        return cve_data['result']['CVE_Items'][0]
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error fetching CVE data for {cve_id}: {e}")
        return {"error": f"HTTP error: {str(e)}"}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error fetching CVE data for {cve_id}: {e}")
        return {"error": f"Connection error: {str(e)}"}
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error fetching CVE data for {cve_id}: {e}")
        return {"error": f"Timeout error: {str(e)}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching CVE data: {e}")
        return {"error": f"Error fetching CVE data: {str(e)}"}

def get_cve_description(cve_data: dict) -> str:
    """
    Extract and return the description of the CVE.
    :param cve_data: The CVE data dictionary.
    :return: A string containing the CVE description.
    """
    try:
        return cve_data['cve']['description']['description_data'][0].get('value', 'Description not available.')
    except (KeyError, IndexError) as e:
        logger.error(f"Error extracting CVE description: {e}")
        return "Description not available."

def get_cve_severity(cve_data: dict) -> str:
    """
    Extract and return the severity of the CVE.
    :param cve_data: The CVE data dictionary.
    :return: A string containing the CVE severity.
    """
    try:
        return cve_data.get('impact', {}).get('baseMetricV3', {}).get('cvssV3', {}).get('baseSeverity',
                   cve_data.get('impact', {}).get('baseMetricV2', {}).get('severity', 'Severity not available.'))
    except KeyError:
        return "Severity not available."
