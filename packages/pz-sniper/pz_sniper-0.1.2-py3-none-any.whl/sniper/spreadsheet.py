import csv

def fileToRows(file):
    rows=[]
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id = row['Identifier']
            type = row['Type']
            region = row['Region']
            rows.append({"id": id, "type": type, "region": region})
    return rows
