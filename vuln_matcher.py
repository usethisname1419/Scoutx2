import json
from logger import print_error
def load_cve_data():
    """
    Loads the CVE data from 'cve_data.json'.
    Returns the data as a dictionary or None if an error occurs.
    """
    try:
        with open("cve_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print_error("CVE data file 'cve_data.json' not found.")
        return None
    except json.JSONDecodeError:
        print_error("CVE data file 'cve_data.json' is corrupted or invalid.")
        return None

def match_vulnerability(service, version=None):
    cve_data = load_cve_data()
    matches = []

    # List of services we care about
    services_to_check = [
        "apache", "ssh", "ftp", "mysql", "rdp",
        "netbios", "smb", "dns", "http-proxy",
        "postgresql", "redis", "elasticsearch", "mongodb", "rabbitmq"
    ]

    # Only proceed if the service is one we care about
    if service.lower() not in services_to_check:
        return matches

    for item in cve_data.get("result", {}).get("CVE_Items", []):
        description = item["cve"]["description"]["description_data"][0]["value"]

        # Match the service name in the description
        if service.lower() in description.lower():
            # Optionally match version if provided
            if version and version in description:
                matches.append({
                    "id": item["cve"]["CVE_data_meta"]["ID"],
                    "description": description
                })
            elif not version:
                matches.append({
                    "id": item["cve"]["CVE_data_meta"]["ID"],
                    "description": description
                })

    return matches
