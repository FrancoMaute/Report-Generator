from dataclasses import field
import json

def load_findings():
    with open("data/findings.json", "r") as file : 
        content = json.load(file)

    return content

content = load_findings()
print(content)