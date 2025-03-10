import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Define the directory to save PDB files
output_dir = "pdb_files"
os.makedirs(output_dir, exist_ok=True)

# Read PDB IDs from the text file
with open("ribosomal_subunits_results.txt", "r") as file:
    pdb_ids = [line.strip() for line in file if line.strip()]

# Base URL for downloading PDB files
base_url = "https://files.rcsb.org/download/{}.pdb"

# Function to download a PDB file
def download_pdb(pdb_id, retries=3):
    url = base_url.format(pdb_id)
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(output_dir, f"{pdb_id}.pdb"), "w") as f:
                    f.write(response.text)
                print(f"Downloaded: {pdb_id}")
                return
            else:
                print(f"Failed to download: {pdb_id}, Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {pdb_id}: {e}")
        time.sleep(2)  # Wait before retrying
    print(f"Failed to download {pdb_id} after {retries} attempts")

# Iterate over PDB IDs and download each file
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_pdb, pdb_ids)
