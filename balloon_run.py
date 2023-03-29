from Bio.PDB import *
import os
import pubchempy as pcp
from datetime import datetime
import shutil
import re
import platform

op_sys = platform.system()

def generate_conformations(cid):
    print("\n+-----------------------+")
    print("|Generating Conformations|")
    print("+-----------------------+\n")

    print("Creating conformations directory....")
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S_conformations")
    new_dir_path = os.path.join(os.getcwd(), date_time_str)
    os.mkdir(new_dir_path)

    print("Retrieving smiles....")
    c = pcp.Compound.from_cid(cid)
    smiles = c.canonical_smiles

    print("Generating conformations....")
    if(op_sys == "Linux"):
        os.system(f"./balloon --nconfs 20 --noGA \"{str(smiles)}\" caffeine.sdf ")
    elif(op_sys == "Windows"):
        os.system(f"balloon --nconfs 20 --noGA \"{str(smiles)}\" caffeine.sdf ")

    f = open("caffeine.sdf", "r")

    conf_list = f.read().split("$$$$")
    for i in range(len(conf_list)-1):
        file = open(f"file_{i+1}.sdf", "w")
        input_sdf = re.sub("^\n", "", conf_list[i])
        file.write(input_sdf)
        file.close()

        print("Using Openbabel to convert .sdf to pdb....")
        os.system(f"obabel -isdf file_{i+1}.sdf -opdb > file_{i+1}.pdb")
        os.remove(f"file_{i+1}.sdf")
        shutil.move(f"file_{i+1}.pdb", new_dir_path)
    
    print("\n+-----------------------+")
    print("|CONFORMATIONS GENERATED|")
    print("+-----------------------+\n")
    
    return smiles
