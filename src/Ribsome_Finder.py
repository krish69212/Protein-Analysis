from rcsbapi.search import TextQuery, AttributeQuery

# Create a TextQuery to search for structures containing the phrase "RIBOSOME"
query1 = TextQuery(value="RIBOSOME")

query2 = AttributeQuery(attribute= "struct_keywords.pdbx_keywords",
                        negation= False,
                        operator= "contains_phrase",
                        value= "RIBOSOME"
)   

# Execute the combined query by calling it as a function
results = (query1 & query2)()

# Check if any results were returned
if not results:
    print("No results found for 'RIBOSOME'.")
else:
    # Open a text file in write mode to store PDB IDs
    with open("ribosomal_subunits_results.txt", "w") as file:
        for rid in results:
            file.write(rid + "\n")