import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

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

def get_severity(cvss):
    if not (isinstance(cvss, int) or isinstance(cvss, float)) or not 0 <= cvss <= 10:
        print("[-]Error: cvss must be a number between 0 and 10")
        return False
    if cvss == 0: return "none"
    if cvss < 4: return "low"
    if cvss < 7: return "medium"
    if cvss < 9: return "high"
    else: return "critical"

def summary(content):
    summary_cvss = {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "none": 0
}
    for finding in content["findings"]:
        cvss = finding['cvss']
        severity = get_severity(cvss)
        summary_cvss[severity] += 1 
    return summary_cvss

def generate_html(content):
    env = Environment(
        loader=FileSystemLoader(base_dir / "templates"),
        autoescape=True
    )

    template = env.get_template("report.html")

    html = template.render(
        project_name=content['project_name'],
        target=content['target']
    )
    return html

html = generate_html(content)

def save_html(html):
    with open(base_dir / "reports" / "report.html", "w") as file:
        file.write(html)
    

save_html(html)
