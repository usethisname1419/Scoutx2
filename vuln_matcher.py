import json


def load_cve_data():
    with open("cve_data.json", "r") as file:
        return json.load(file)


def match_vulnerability(service, version):
    cve_data = load_cve_data()
    matches = []

    # List of services we care about
    services_to_check = ["apache", "ssh", "ftp", "mysql", "rdp"]

    # Only proceed if the service is one we care about
    if service.lower() not in services_to_check:
        return matches

    for item in cve_data.get("result", {}).get("CVE_Items", []):
        description = item["cve"]["description"]["description_data"][0]["value"]

        # Match the service name in the description (no version check)
        if service.lower() in description.lower():
            matches.append({
                "id": item["cve"]["CVE_data_meta"]["ID"],
                "description": description
            })

    return matches


