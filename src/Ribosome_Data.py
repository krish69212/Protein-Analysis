import pandas as pd
from rcsbapi.data import DataQuery as Query

# Read PDB IDs from the text file.
with open("Protein-Analysis-1/src/ribosomal_subunits_results.txt", "r") as file:
    pdb_ids = [line.strip() for line in file if line.strip()]

# Define the fields to retrieve.
fields = [
    "rcsb_id",                                 # PDB ID
    "struct.title",                            # Structure title
    "exptl.method",                            # Experimental method
    "rcsb_accession_info.initial_release_date",  # Release date
    "rcsb_entry_info.resolution_combined",     # Resolution
    "rcsb_entry_info.polymer_entity_count",    # Number of polymer entities
    "rcsb_entry_info.nonpolymer_entity_count", # Number of non-polymer entities
    "rcsb_entry_info.molecular_weight"         # Molecular weight
]

# Initialize a list to store records.
records = []

# Fetch data for each PDB ID.
for index, pdb_id in enumerate(pdb_ids, start=1):
    print(f"Processing {index}/{len(pdb_ids)}: {pdb_id}")
    q = Query(input_type="entries", input_ids=[pdb_id], return_data_list=fields)
    
    try:
        result = q.exec()
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")
        continue  # Skip to the next PDB ID if an error occurs

    entry = result.get("data", {}).get("entries", [{}])[0]

    # Extract data safely.
    rcsb_id = entry.get("rcsb_id", "")
    title = entry.get("struct", {}).get("title", "")

    # Ensure experimental method is extracted safely
    method_list = entry.get("exptl", [])
    method = method_list[0].get("method", "") if isinstance(method_list, list) and method_list else ""

    release_date = entry.get("rcsb_accession_info", {}).get("initial_release_date", "")

    # Handle resolution correctly
    resolution_list = entry.get("rcsb_entry_info", {}).get("resolution_combined", [])
    resolution = resolution_list[0] if isinstance(resolution_list, list) and resolution_list else None

    # Handle counts and molecular weight safely
    polymer_count = entry.get("rcsb_entry_info", {}).get("polymer_entity_count", 0) or 0
    nonpolymer_count = entry.get("rcsb_entry_info", {}).get("nonpolymer_entity_count", 0) or 0
    molecular_weight = entry.get("rcsb_entry_info", {}).get("molecular_weight", 0.0) or 0.0

    # Append the extracted data to records.
    records.append({
        "PDB ID": rcsb_id,
        "Title": title,
        "Experimental Method": method,
        "Release Date": release_date,
        "Resolution": resolution,
        "Polymer Entity Count": polymer_count,
        "Non-Polymer Entity Count": nonpolymer_count,
        "Molecular Weight": molecular_weight
    })

# Create a DataFrame and export to Excel.
df = pd.DataFrame(records)
df.to_excel("rcsb_statistical_data_enhanced.xlsx", index=False)
print("Data successfully written to rcsb_statistical_data_enhanced.xlsx")