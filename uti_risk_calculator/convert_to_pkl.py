import json
import pickle

# Path to the JSON file
json_file_path = 'uti_risk_calculator/model_config.json'
# Path for the output PKL file
pkl_file_path = 'uti_risk_calculator/model_config.pkl'

try:
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        model_config = json.load(f)

    # Save the data as a PKL file
    with open(pkl_file_path, 'wb') as f:
        pickle.dump(model_config, f)

    print(f"Successfully converted {json_file_path} to {pkl_file_path}")

except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}") 