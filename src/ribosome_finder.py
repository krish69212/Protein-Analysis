import os
import pypdb
import pandas as pd

# Search for ribosomes in the PDB
print("Searching for ribosomes in the PDB...")
ribosome_results = pypdb.Query("ribosome").search()

print(f"Found {len(ribosome_results)} ribosome structures")

# Create a list to store information about each ribosome
ribosome_data = []

# For each PDB ID, get additional information
for i, pdb_id in enumerate(ribosome_results):
    print(f"Processing {i+1}/{len(ribosome_results)}: {pdb_id}")
    try:
        # Get summary information for this PDB entry
        info = pypdb.get_info(pdb_id)
        
        # Extract relevant information
        title = info.get('title', 'N/A')
        resolution = info.get('resolution', 'N/A')
        deposition_date = info.get('deposition_date', 'N/A')
        
        # Get the structure type (e.g., protein, RNA, DNA)
        structure_info = pypdb.get_all_info(pdb_id)
        entity_info = structure_info.get('polymer', {}).get('entity', [])
        structure_types = []
        
        if isinstance(entity_info, list):
            for entity in entity_info:
                if 'type' in entity:
                    structure_types.append(entity['type'])
        elif isinstance(entity_info, dict) and 'type' in entity_info:
            structure_types.append(entity_info['type'])
            
        structure_type = ', '.join(set(structure_types)) if structure_types else 'N/A'
        
        # Add to our data list
        ribosome_data.append({
            'PDB_ID': pdb_id,
            'Title': title,
            'Resolution': resolution,
            'Deposition_Date': deposition_date,
            'Structure_Type': structure_type
        })
        
    except Exception as e:
        print(f"Error processing {pdb_id}: {e}")
        # Still add the PDB ID to our list, but with incomplete information
        ribosome_data.append({
            'PDB_ID': pdb_id,
            'Title': 'Error retrieving data',
            'Resolution': 'N/A',
            'Deposition_Date': 'N/A',
            'Structure_Type': 'N/A'
        })

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(ribosome_data)

# Sort by deposition date (newest first)
try:
    df['Deposition_Date'] = pd.to_datetime(df['Deposition_Date'], errors='coerce')
    df = df.sort_values('Deposition_Date', ascending=False)
except:
    print("Warning: Could not sort by date, using original order")

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save to CSV file
output_file = "data/ribosome_structures.csv"
df.to_csv(output_file, index=False)
print(f"Saved ribosome data to {output_file}")

# Also save just the PDB IDs to a text file
with open("data/ribosome_pdb_ids.txt", "w") as f:
    for pdb_id in df['PDB_ID']:
        f.write(f"{pdb_id}\n")
print("Saved PDB IDs to data/ribosome_pdb_ids.txt")
