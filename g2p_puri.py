from Bio.PDB import *
import re
import os
import requests

def gene_to_pdb_purification(gene_list):
    print("\n+---------------------+")
    print("|PDB Retrieval Running|")
    print("+---------------------+\n")
    for gene_name in gene_list:
        print("Generating query for PDB API....")
        query = {
            "query": {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_entity_source_organism.rcsb_gene_name.value",
                    "operator": "exact_match",
                    "value": gene_name
                }
            },
            "return_type": "entry"
        }

        print("Querying PDB Database....")
        url = "https://search.rcsb.org/rcsbsearch/v2/query"
        response = requests.post(url, json=query)
        json_response = response.json()

        print("Getting PDB IDs for TOP 3 genes")
        pdb_ids = [hit["identifier"] for hit in json_response["result_set"]]

        io = PDBIO()
        pdbID = pdb_ids[0]
        pdbl = PDBList()
        pdbl.retrieve_pdb_file(pdbID, pdir = '.', file_format = 'pdb')
        parser = PDBParser(PERMISSIVE = True, QUIET = True)
        file = "pdb"+pdbID+".ent"
        data = parser.get_structure(pdbID,file)
        file_rename = re.sub("ent", "pdb", file)
        os.rename(file, file_rename)

        model = data[0]
        residue_to_remove = []
        chain_to_remove = []

        for chain in model:
            for residue in chain:
                if residue.id[0] != ' ':
                    residue_to_remove.append((chain.id, residue.id))
            if len(chain) == 0:
                chain_to_remove.append(chain.id)
        for residue in residue_to_remove:
            model[residue[0]].detach_child(residue[1])
        for chain in chain_to_remove:
            print(f"chain: {chain}")
            model.detach_child(chain)

        io.set_structure(model)
        io.save("model"+".pdb")

        for chains in model.get_chains():
            io.set_structure(chains)
            io.save(f"chain_{str(chains)[-2]}_{pdb_ids[0]}.pdb")

        for chain in model.get_chains():
            print(f"Chain ID: {str(chain)[-2]}")
            
        user_chain_input = input("Enter chains you want to remove separate by (,): ")
        user_input_list = user_chain_input.split(",")

        if user_input_list > 0:
            for inputs in user_input_list:
                model.detach_child(inputs)

            io.set_structure(model)
            io.save(f"model_{pdb_ids[0]}_without_chain{str(user_input_list)}.pdb")
        else:
            io.set_structure(model)
            io.save(f"model_with_all_chains.pdb")