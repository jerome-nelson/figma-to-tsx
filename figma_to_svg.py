import os
import requests
import json
import datetime;
from dotenv import load_dotenv

# These variables should be set in Gitlab
# FIGMA_API_TOKEN: Read only Token
# FIGMA_FILE_ID  : Taken from FIGMA URL
load_dotenv()
FIGMA_API_TOKEN = os.getenv("FIGMA_API_TOKEN")
FIGMA_FILE_ID = os.getenv("FIGMA_FILE_ID")
FIGMA_FILE_GROUP = "ICON SHEET"

# Figma API headers
headers = {
    "X-Figma-Token": FIGMA_API_TOKEN
}

def extract_ids_from_icon_sheet(icon_sheet):
    node_map = {}
    if isinstance(icon_sheet, dict) and "children" in icon_sheet:
        for child in icon_sheet["children"]:
            if "id" in child:
                # What about if there is no name in response? (Is that possible)?
                node_map[child["id"]] = child["name"]
    
    return node_map

def find_sheet(data):
    if isinstance(data, dict):
        if data.get("name") == FIGMA_FILE_GROUP:
            print("🙃 Found the sheet")
            return data

    if isinstance(data, dict) and "children" in data:
        for child in data["children"]:
            result = find_sheet(child)
            if result:
                return result

    return None

def generate_svgs():
    print("🔍 Fetching nodes from Figma...")

    # Calls the Figma API and returns Document response
    url = f"https://api.figma.com/v1/files/{FIGMA_FILE_ID}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"generated/figma_response_{timestamp}.json"

        # Create a folder if it doesn't exist
        os.makedirs("generated", exist_ok=True)

        with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"😃 Response saved to {filename}")
        sheet = find_sheet(data.get("document", {}))
        node_map = extract_ids_from_icon_sheet(sheet)
        ids = list(node_map.keys())
        svg_urls = get_svg_urls(ids)

        if svg_urls:
            print("⬇️ Downloading SVG files...")
            download_svgs(node_map, svg_urls)
            print("✅ All SVGs downloaded!")
    else:
        print("Error fetching Figma file:", response.status_code, response.text)
        return None

def get_svg_urls(node_ids):
    node_param = ",".join(node_ids)
    url = f"https://api.figma.com/v1/images/{FIGMA_FILE_ID}?ids={node_param}&format=svg"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("images", {})
    else:
        print("Error fetching SVGs:", response.status_code, response.text)
        return None


def download_svgs(node_map, svg_urls):
    os.makedirs("generated/svgs", exist_ok=True)
    
    for node_id, svg_url in svg_urls.items():
        response = requests.get(svg_url)
        if response.status_code == 200:
            with open(f"generated/svgs/{node_map[node_id]}.svg", "wb") as f:
                f.write(response.content)
            print(f"✅ Saved: generated/svgs/{node_map[node_id]}.svg")
        else:
            print(f"❌ Failed to download SVG for node {node_id}")

    
