"""Convert OPML file to YAML file.

TODO:
- check if podcasts still exist
"""
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml

root_folder = Path(__file__).parents[1]

opml_file = root_folder / "OPML_export_20250301_202833.opml"

output_yaml = root_folder / "_data" / "podcasts.yml"

def parse_opml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    podcasts = []
    
    for outline in root.findall(".//outline"):
        podcast = {
            "title": outline.get("text"),
            "type": outline.get("type"),
            "rss_url": outline.get("xmlUrl"),
            "html_url": outline.get("htmlUrl"),
            "image_url": outline.get("imageUrl")
        }
        if podcast["title"] != "Comments on":
            podcasts.append(podcast)
    
    return podcasts

def save_to_yaml(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


podcasts = parse_opml(opml_file)
save_to_yaml(podcasts, output_yaml)

