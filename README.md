# Scoutx2: A Vulnerability Scanning Tool

Scoutx2 is an updated version of my original Scout tool, designed to quickly scan valid IPs from a given region and check them for vulnerabilities based on the latest CVE data published by NIST.


I created this tool as a proof of concept (PoC) after wondering, "How do hackers find so many vulnerable hosts so fast when a new CVE is published?" Scoutx2 answers that by automating the process of scanning IPs for vulnerabilities tied to recently published CVEs.


# Features:

Scan local or regional networks: You can select between scanning a local IP (127.0.0.1) or generate a list of IPs from a specified region (North America or Europe).

Fetch the latest CVE data: Automatically pulls CVE data from NIST, covering the last 25 days.

Scan 1-100 IPs: Choose how many IPs to scan between 1 and 100.

Vulnerability matching: Matches the CVE data against services like Apache, MySQL, SSH, and more to identify vulnerabilities.

Scan report generation: Creates a detailed report of findings, including vulnerable services and any related CVEs.


# Installation

Clone this repository:

```
git clone https://github.com/usethisname1419/scoutx2.git
cd scoutx2
```

Install required dependencies

`pip install -r requirements.txt`


# Usage

To start the scan, simply run:

`python3 coordinator.py`

# Workflow:

Select scan type: Local or Regional.

If Regional, select the region (North America or Europe) and select your OS (Windows or Linux).

Choose the number of IPs to scan (1-100).

The tool will fetch the latest CVE data from NIST for the last 25 days.

It will scan the selected IPs for open ports and match them against known vulnerabilities.

A report is generated at the end with detailed results.

# Support

As always, if you appreciate the tool, I accept donations to support further development.

BTC: bc1qtezfajhysn6dut07m60vtg0s33jy8tqcvjqqzk


