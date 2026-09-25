import json
import re
import sys
from pathlib import Path

import requests

BASE_URL = "https://mausamsankalp.imd.gov.in"
TAS_URL = f"{BASE_URL}/tas/tas"


def extract_csrf(html):
    match = re.search(
        r'name="csrf_token"[^>]*value="([^"]+)"',
        html
    )
    if not match:
        raise RuntimeError("CSRF token not found")
    return match.group(1)


def extract_graphs(html):
    match = re.search(
        r"var graphs = (\{.*?\});",
        html,
        re.DOTALL
    )
    if not match:
        raise RuntimeError("Temperature graph data not found")

    return json.loads(match.group(1))


def fetch_temperature(district, block):
    session = requests.Session()

    response = session.get(TAS_URL, timeout=30)
    response.raise_for_status()

    csrf_token = extract_csrf(response.text)

    payload = {
        "State": "TN",
        "District": district,
        "Block": block,
        "rfsubmit": "Submit",
        "csrf_token": csrf_token,
    }

    response = session.post(
        TAS_URL,
        data=payload,
        timeout=30,
    )
    response.raise_for_status()

    graphs = extract_graphs(response.text)

    result = {}

    for item in graphs["data"]:
        name = item["name"].strip()

        result[name] = {
            "years": item["x"],
            "values": item["y"],
        }

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/imd_heat_extract.py DISTRICT BLOCK")
        sys.exit(1)

    district = sys.argv[1]
    block = sys.argv[2]

    data = fetch_temperature(district, block)

    safe_name = district.lower().replace(" ", "_")

    output = Path("data/heat") / f"{safe_name}_temperature.json"

    output.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    print(f"Saved: {output}")