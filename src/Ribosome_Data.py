import pandas as pd
from rcsbapi.data import DataQuery as Query

# Read PDB IDs from the text file.
with open("ribosomal_subunits_results.txt", "r") as file:
    pdb_ids = [line.strip() for line in file if line.strip()]

# Define the fields to retrieve (organism removed).
fields = [
    "rcsb_id",                                 # PDB ID
    "struct.title",                            # Structure title
    "exptl.method",                            # Experimental method
    "rcsb_accession_info.initial_release_date",  # Release date
    "rcsb_entry_info.resolution_combined"      # Resolution (if applicable)
]

records = []
for pdb_id in pdb_ids:
    q = Query(input_type="entries", input_ids=[pdb_id], return_data_list=fields)
    result = q.exec()
    # Get the first entry (if available)
    entry = result.get("data", {}).get("entries", [{}])[0]
    
    rcsb_id = entry.get("rcsb_id", "")
    title = entry.get("struct", {}).get("title", "")
    
    # Experimental method is expected to be in a list.
    method = ""
    exptl = entry.get("exptl")
    if isinstance(exptl, list) and exptl:
        method = exptl[0].get("method", "")
        
    release_date = entry.get("rcsb_accession_info", {}).get("initial_release_date", "")
    resolution = entry.get("rcsb_entry_info", {}).get("resolution_combined", "")
    
    records.append({
        "PDB ID": rcsb_id,
        "Title": title,
        "Experimental Method": method,
        "Release Date": release_date,
        "Resolution": resolution
    })

# Create a DataFrame and export to Excel.
df = pd.DataFrame(records)
df.to_excel("rcsb_statistical_data.xlsx", index=False)
print("Data successfully written to rcsb_statistical_data.xlsx")
