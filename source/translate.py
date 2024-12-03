import os
import pandas as pd

# Directory containing the CSV files
directory = "./"  # Replace with the actual directory containing the CSV files

# Load the Pokémon Chinese names dataset
chinese_names_file = "pokemon_chinese_names_all_generations.csv"
chinese_names = pd.read_csv(chinese_names_file)

# Map English to Traditional Chinese names
name_mapping = dict(zip(chinese_names['English Name'], chinese_names['Traditional Chinese']))

# Process all CSV files in the directory, except the Chinese names file
for filename in os.listdir(directory):
    if filename.endswith(".csv") and filename != "pokemon_chinese_names_all_generations.csv" and not filename.startswith("updated"):
        file_path = os.path.join(directory, filename)
        
        # Load the CSV file
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Failed to read {filename}: {e}")
            continue
        

        # Check if the file has a 'Pokemon' column
        if 'Pokemon' in df.columns:
            # Add a new column for Traditional Chinese names
            df['Traditional Chinese'] = df['Pokemon'].map(name_mapping)
            
            # Save the updated file
            updated_file_path = os.path.join(directory, f"updated_{filename}")
            df.to_csv(updated_file_path, index=False, encoding='utf-8-sig')
            print(f"Updated file saved to '{updated_file_path}'")
        else:
            print(f"File '{filename}' does not have a 'Pokemon' column. Skipping.")

print("Processing complete.")
