import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent


def load_findings():
    with open(base_dir / "data" / "findings.json", "r") as file : 
        content = json.load(file)

    return content

content = load_findings()



def validate_required_top_fields(content):
    if not isinstance(content, dict):
        print("[-] Error: Expected a dictionary")
        return False

    required_top_fields = [
        "project_name",
        "target",
        "findings"
    ]

    for field in required_top_fields:
        if field not in content:
            print(f"[-] Error: Missing {field}")
            return False

    return True



def validate_findings(content):
    required_fields = [
        "title",
        "cvss",
        "description",
        "impact",
        "remediation"
    ]
    
    if not isinstance(content["findings"], list):
                print("[-]Error: Findings must be a list")
                return False

    for finding in content["findings"]:
        
        for field in required_fields:
            if field not in finding:
                print(f"[-] Error: Missing {field}")
                return False

        if not (isinstance(finding["cvss"], int) or isinstance(finding["cvss"], float)):
            print("[-] Error: CVSS must be a number")
            return False

        if finding["cvss"] < 0 or finding["cvss"] > 10:
            print("[-] Error: Invalid CVSS")
            return False
        
        


        

    return True




if validate_required_top_fields(content) and validate_findings(content):
    print("[+] Valid report data")
else:
    print("[-] Invalid report data")