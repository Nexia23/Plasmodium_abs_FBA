import json

# Path to the Jupyter notebook file
notebook_path = 'notebook_cleaner.ipynb'

# Read the notebook file
with open(notebook_path) as f:
    nb_json = json.load(f)

# Clear the output of each cell
for cell in nb_json['cells']:
    if 'outputs' in cell:
        cell['outputs'] = []
    if 'execution_count' in cell:
        cell['execution_count'] = None

notebook_path = 'new_notebook_cleaner.ipynb'
# Save the modified notebook file
with open(notebook_path, 'w') as f:
    json.dump(nb_json, f)