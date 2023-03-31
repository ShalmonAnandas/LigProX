# LigProX
Cross Platform commandline software to Automate the time consuming process before docking

---

## Overview
The project automates the process of extracting protein targets for a given Pubchem CID. It performs the following steps:

- Generate conformations of the given Pubchem CID using Balloon
- Scrapes SwissTargetPrediction for gene names related to the Pubchem CID
- Get protein-protein interaction network by scraping String DB
- Extracting Top 3 genes from this network by use of Kmeans Clustering
- Retrieve PDB files corresponding to these genes
- Purifying thee PDB files (Removing water molecules, Hetero Atoms, Chains {User selected})
- Move generated files to a timestamped folder.

## Usage
- REQUIRES CHROME TO RUN!!!
- Install requirements

> `pip install -r requirements.tst`

- Run the python file main.py.
- Software will prompt you accordingly

## Documentation for Development (Better coming soon)

- main.py
    - Core file that brings it all together
- balloon_run.py
    - Runs conformational search on the given Pubchem CID and gives a total of 20 conformations using Balloon software
    - MMFF94.mff forcefield file and balloon.exe is included (balloon for linux support)
- swiss_target_scrapper.py
    - Scrapes [SwissTargetPrediction](http://www.swisstargetprediction.ch/)
- gene_names.py
    - Extracts gene names obtained into a separate txt file
- string_db_scrapper.py
    - Scrapes [Strind-DB](https://string-db.org/)
- g2p_puri.py
    - Retrieves PDB structures and purifies them

## This project uses the following packages:

- [Pandas](https://pandas.pydata.org/)
- [Selenium](https://www.selenium.dev/)
- [Biopython](https://biopython.org/)
- [Pubchempy](https://pubchempy.readthedocs.io/en/latest/)
- [Balloon](http://users.abo.fi/mivainio/balloon/change_log.htm)


## License
This project is licensed under the MIT License.