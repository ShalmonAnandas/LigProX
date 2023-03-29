import csv

def get_gene_names():
    print("\n+---------------------+")
    print("|Extracting Gene Names|")
    print("+---------------------+\n")
    common_names = []

    print("Scanning SwissTargetPrediction.csv....")
    with open('SwissTargetPrediction.csv', 'r') as file:
        reader = csv.DictReader(file)
        common_names = []
        for row in reader:
            if float(row['Probability*']) != 0:
                common_names.append(row['Common name'])

    print("Extracting Gene Names into txt file....")
    with open('swiss_target_gene_names.txt', 'w') as file:
        for names in common_names:
            file.write(names)
            file.write("\n")

    print("\n+------------------------------+")
    print("|Finished Extracting Gene Names|")
    print("+------------------------------+\n")
    
    return common_names