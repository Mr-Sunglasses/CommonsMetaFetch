from traceback import print_tb

import requests
import os
import re
import csv

def parse_filename(s: str) -> str:
    if "https://" in s:
        s = s.split("/")[-1]

    if s.startswith("File:"):
        s = s[len("File:") :]

    s = s.replace(" ", "_")

    s = re.sub(r"[^a-zA-Z0-9_.]", "", s)

    if not s.startswith("_"):
        s = s.lstrip("_")

    return s



def fetch_metadata(file_title):
    base_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "imageinfo",
        "iiprop": "timestamp|user|extmetadata",
        "titles": f"File:{file_title}",
        "format": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    page = next(iter(data["query"]["pages"].values()))
    if "imageinfo" in page:
        return page["imageinfo"][0]
    return {}


def filter_image_metadata(metadata):
    filtered_data = {
        "Description": metadata["extmetadata"].get("ImageDescription", {}).get("value"),
        "Creation Date": metadata["extmetadata"]
        .get("DateTimeOriginal", {})
        .get("value"),
        "Author": metadata["extmetadata"].get("Artist", {}).get("value"),
        "License Information": {
            "License": metadata["extmetadata"].get("License", {}).get("value"),
            "License URL": metadata["extmetadata"].get("LicenseUrl", {}).get("value"),
            "Usage Terms": metadata["extmetadata"].get("UsageTerms", {}).get("value"),
        },
    }
    return filtered_data


def write_dict_list_to_tsv(data_list, file_name):
    with open(file_name, 'w', newline='') as file:
        fieldnames = ['Description', 'Creation Date', 'Author', 'License', 'License URL', 'Usage Terms']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')

        writer.writeheader()

        for data in data_list:
            flattened_data = {
                'Description': data['Description'],
                'Creation Date': data['Creation Date'],
                'Author': data['Author'],
                'License': data['License Information']['License'],
                'License URL': data['License Information']['License URL'],
                'Usage Terms': data['License Information']['Usage Terms']
            }
            writer.writerow(flattened_data)

    print(f"TSV file '{file_name}' written successfully.")


def parse_csv_data_and_write_tsv(csv_file_path):
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"The File {csv_file_path} not found")

    with open(csv_file_path, "r") as csv_file:
        data = []
        reader = csv.reader(csv_file)
        for row in reader:
            for entry in row:
                parsed_entry = parse_filename(entry.lstrip())
                metadata = fetch_metadata(parsed_entry)
                filtered_metadata = filter_image_metadata(metadata)
                data.append(filtered_metadata)
        write_dict_list_to_tsv(data, "output.tsv")


def parse_tsv_data_and_write_tsv(tsv_file_path):
    if not os.path.exists(tsv_file_path):
        raise FileNotFoundError(f"The File {tsv_file_path} not found")

    with open(tsv_file_path, "r") as tsv_file:
        data = []
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            for entry in row:
                parsed_entry = parse_filename(entry.lstrip())
                metadata = fetch_metadata(parsed_entry)
                filtered_metadata = filter_image_metadata(metadata)
                data.append(filtered_metadata)

        write_dict_list_to_tsv(data, "output.tsv")

    print(f"TSV file 'output_from_tsv.tsv' written successfully.")