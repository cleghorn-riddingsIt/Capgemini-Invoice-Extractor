from bs4 import BeautifulSoup

# Open the HTML file
with open('Invoices\\Faktura_peppol_1018428.html', 'r',encoding='utf-8') as f:
    html = f.read()

# Parse the HTML using Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Extract all tables from the HTML
tables = soup.find_all('table')

# Define a data class to represent a table
from typing import List

class Table:
    def __init__(self, caption: str, rows: List[List[str]]):
        self.caption = caption
        self.rows = rows

table_objects = []
for table in tables:
    # Extract the table caption
    caption_element = table.find('caption')
    caption = caption_element.text if caption_element else None
    # Extract the table rows
    rows = []
    for row in table.find_all('tr'):
        row_cells = [cell.text for cell in row.find_all('td')]
        rows.append(row_cells)
        
    # Create a Table object and add it to the list
    table_object = Table(caption=caption, rows=rows)
    table_objects.append(table_object)
    
print(table_objects)