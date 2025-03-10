import os

# Define the directory containing PDB files
pdb_dir = "Protein-Analysis-1\pdb_files"
size_limit = 1500 * 1024  # Convert KB to bytes (4000 KB = 6MB)

# Iterate over files in the directory
for filename in os.listdir(pdb_dir):
    file_path = os.path.join(pdb_dir, filename)
    
    # Check if it's a file and get its size
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)  # Size in bytes
        
        if file_size > size_limit:
            os.remove(file_path)
            print(f"🗑️ Deleted: {filename} ({file_size / 1024:.2f} KB)")
        else:
            print(f"✅ Kept: {filename} ({file_size / 1024:.2f} KB)")
