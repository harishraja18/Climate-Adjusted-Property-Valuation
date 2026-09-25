import json
import time
from pathlib import Path

import requests


BASE_URL = "https://mausamsankalp.imd.gov.in"
TAS_URL = f"{BASE_URL}/tas/tas"
BLOCK_URL = f"{BASE_URL}/getblock"


def extract_csrf(html):
    import re

    match = re.search(
        r'name="csrf_token"[^>]*value="([^"]+)"',
        html
    )

    if not match:
        raise RuntimeError("CSRF token not found")

    return match.group(1)


def extract_graphs(html):
    import re

    match = re.search(
        r"var graphs = (\{.*?\});",
        html,
        re.DOTALL
    )

    if not match:
        raise RuntimeError("Temperature graph data not found")

    return json.loads(match.group(1))


def get_blocks(session, district):
    response = session.post(
        BLOCK_URL,
        data={
            "id": district,
            "state": "TN",
        },
        timeout=30,
    )

    response.raise_for_status()

    return [
        item["id"]
        for item in response.json()["District"]
    ]


def fetch_temperature(session, district, block):
    response = session.get(
        TAS_URL,
        timeout=30,
    )

    response.raise_for_status()

    csrf_token = extract_csrf(response.text)

    response = session.post(
        TAS_URL,
        data={
            "State": "TN",
            "District": district,
            "Block": block,
            "rfsubmit": "Submit",
            "csrf_token": csrf_token,
        },
        timeout=30,
    )

    response.raise_for_status()

    graphs = extract_graphs(response.text)

    result = {}

    for item in graphs["data"]:
        result[item["name"].strip()] = {
            "years": item["x"],
            "values": item["y"],
        }

    return result


def main():
    districts = [
        "Erode",
    ]

    output_dir = Path("data/heat/imd")
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for district in districts:

        # Fresh session for every district
        session = requests.Session()

        print(f"\nDistrict: {district}")

        try:
            blocks = get_blocks(
                session,
                district,
            )

            print(f"Blocks found: {len(blocks)}")

        except Exception as error:
            print(f"  ERROR getting blocks: {error}")
            continue

        district_dir = (
            output_dir
            / district.lower().replace(" ", "_")
        )

        district_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for block in blocks:

            print(f"  Fetching: {block}")

            try:
                data = fetch_temperature(
                    session,
                    district,
                    block,
                )

                output = district_dir / (
                    f"{block.lower().replace(' ', '_')}.json"
                )

                output.write_text(
                    json.dumps(
                        data,
                        indent=2,
                    ),
                    encoding="utf-8",
                )

                print(f"  Saved: {output}")

            except Exception as error:
                print(f"  ERROR: {error}")

            # Small pause between requests
            time.sleep(1)


if __name__ == "__main__":
    main()