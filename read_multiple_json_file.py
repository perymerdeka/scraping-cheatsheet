import json
import os
import glob

# directory PATH
json_dir = os.path.dirname(os.path.realpath(__file__))

# glob read file 
file_results = sorted(glob.glob(os.path.join(json_dir, 'results/*.json')))
# Check Dir PATH
print(file_results)

datas = []

# Looping content directory
for file in file_results:
    print('Reading File: {}'.format(file))
    with open(file, 'r') as json_file:
        json_data = json.load(json_file)
    datas.append(json_data)
