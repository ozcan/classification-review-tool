import csv
import json

# Open the input JSON file
with open('output.json') as json_file:
    data = json.load(json_file)

# Create a CSV file for writing
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(['filename', 'label'])

    # Loop through each key in the JSON data
    for label, filenames in data.items():
        # Loop through each filename in the list
        for filename in filenames:
            # Write the filename and label to the CSV file
            writer.writerow([filename, label])

print('CSV file created successfully.')