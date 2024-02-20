from bs4 import BeautifulSoup
import requests
import pandas as pd
import itertools

# URL of the Wikipedia page to scrape
url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"

page = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser')

# Find the table containing the desired data by class name
table = soup.find("table", class_ = "wikitable sortable")

# Extract column titles from table headers
world_titles = table.find_all('th')
world_table_titles = [title.text.strip() for title in world_titles]

# Clean up column titles: trim extra spaces, remove "[note 1]" from the last title
world_table_titles = world_table_titles[:7]
world_table_titles[-1] = world_table_titles[-1].replace("[note 1]", "")

df = pd.DataFrame(columns = world_table_titles)

# Extract row data from the table
column_data = table.find_all("tr")

# Iterate over each row of the table (skipping the header rows), extract text from each cell
# Keep only the first 7 elements of each row
# Append the row data to the DataFrame
for row in column_data[2:]:
    row_data = row.find_all("td")
    individial_row_data = [data.text.strip() for data in row_data]
    individial_row_data = individial_row_data[:7]
    length = len(df)
    df.loc[length] = individial_row_data

# Shift the DataFrame columns one position to the right
df = df.shift(axis=1)
df.iloc[:, 0] = ""

# Create csv file
df.to_csv(r"D:\DL", index=False) 