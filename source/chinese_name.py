import requests
from bs4 import BeautifulSoup
from html import unescape
import pandas as pd

# Fetch the webpage
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Chinese_Pok%C3%A9mon_names"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Set the correct encoding explicitly
response.encoding = 'utf-8'

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables corresponding to Pokémon generations
tables = soup.find_all('table', {'class': 'roundy'})
if not tables:
    print("No tables found. Check the webpage structure.")
    exit()

data = []

# Process each table
for table in tables:
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 5:  # Ensure enough columns are present
            english_name = unescape(cols[2].text.strip())
            traditional_chinese = unescape(cols[3].text.strip())
            data.append({"English Name": english_name, "Traditional Chinese": traditional_chinese})

# Check if data was extracted
if not data:
    print("No data extracted. Verify the table parsing logic.")
    exit()

# Convert to DataFrame
df = pd.DataFrame(data)

# Save the data as UTF-8 with BOM for compatibility with Excel and others
output_file = 'pokemon_chinese_names_all_generations.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Data from all generations saved to '{output_file}'.")
