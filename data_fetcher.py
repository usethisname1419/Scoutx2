import requests
import json
from datetime import datetime, timedelta
from logger import print_info, print_error
def fetch_cve_data():
    # Calculate date range for the last week
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=25)

    # Format dates in ISO 8601
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    # API URL and parameters
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "pubStartDate": start_date_str,
        "pubEndDate": end_date_str,
        "startIndex": 0,
        "resultsPerPage": 1000  # Fetch up to 1000 results at a time
    }

    # Fetch data
    print_info(f"Fetching CVEs published between {start_date_str} and {end_date_str}.")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        cve_data = response.json()
        with open("cve_data.json", "w") as file:
            json.dump(cve_data, file, indent=4)
        print_info("CVE data fetched and saved to 'cve_data.json'.")
    else:
        print_error(f"Failed to fetch CVE data. HTTP Status Code: {response.status_code}")

