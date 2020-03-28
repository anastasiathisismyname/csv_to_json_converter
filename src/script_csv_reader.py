import csv
import json

csvFilePath = 'csv_file.csv'

jsonFilePath = 'json_file_name.json'

data = {}

with open(csvFilePath) as csv_file:
    csvReader = csv.DictReader(csv_file)
    for rows in csvReader:
        fn = rows["FirstName"]
        ln = rows["LastName"]
        id = rows["IDNumber"]
        m = rows["Message"]
        data[fn] = rows
        data[ln] = rows
        data[m] = rows
        data[id] = rows

with open(jsonFilePath, 'w') as json_file:
    json_file.write(json.dumps(data, indent=4))