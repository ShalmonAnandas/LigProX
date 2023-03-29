import os
import shutil
from datetime import datetime

from balloon_run import generate_conformations
from swiss_target_scrapper import get_csv
from gene_names import get_gene_names
from string_db_scrapper import get_ppi_network
from g2p_puri import gene_to_pdb_purification

cid = input("Enter a Pubchem CID: ")
smiles = generate_conformations(cid)
get_csv(smiles)

home_dir = os.path.expanduser("~")
file_path = f"{home_dir}\\Downloads\\SwissTargetPrediction.csv"
shutil.move(file_path, f"{os.getcwd()}\\SwissTargetPrediction.csv")

gene_name_list = get_gene_names()
genes_list = get_ppi_network(gene_name_list)
gene_to_pdb_purification(genes_list)

print("Moving files generated during run to timestamped folder....")
now = datetime.now()
date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S_PDB")
new_dir_path = os.path.join(os.getcwd(), date_time_str)
os.mkdir(new_dir_path)
source_dir = os.getcwd()
dest_dir = new_dir_path
for file_name in os.listdir(source_dir):
    if file_name.endswith('.pdb') or file_name.endswith('.txt') or file_name.endswith('.tsv') or file_name.endswith('.csv'):
        source_file = os.path.join(source_dir, file_name)
        dest_file = os.path.join(dest_dir, file_name)
        shutil.move(source_file, dest_file)

print("\n+--------+")
print("|FINSIHED|")
print("+--------+\n")