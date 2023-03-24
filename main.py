from bs4 import BeautifulSoup
from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict
from datetime import datetime
from typing import Dict



# Open the HTML file
with open('Invoices\\Faktura_peppol_1018429.html', 'r',encoding='utf-8',newline='\n') as f:
    rawhtml = f.read()
html=rawhtml.replace('\n','').replace('\xa0','')# cleans up the text and removes weird spaces


#html=html.replace('\xa','')

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

def convert_to_float(value: str) -> float:
    try:
        cleaned_string = value.replace(",", ".").replace("%", "")
        return float(cleaned_string)
    except ValueError:
        raise ValueError(f"{value} is not a valid float")


def extract_check_items(row: list) -> dict:
    if len(row) < 8:
        raise ValueError("Row must have at least 8 elements")

    check_items_row = {}
    consultant_details = str(row[1]).split()
    check_items_row['summary'] = consultant_details[0]
    check_items_row['linkeditem'] = ""
    check_items_row['hours'] = convert_to_float(row[3])
    check_items_row['rate'] = convert_to_float(row[5])
    check_items_row['total_net'] = convert_to_float(row[6])
    check_items_row['tax_rate'] = convert_to_float(row[7])
    check_items_row['total_gross'] = convert_to_float(row[8])
    return check_items_row
    
    


def extract_invoice(invoice:Table,checkitems:Table)->Dict:
    invoice_dict={}
    lineitems=[]
    linked_workitem_list=[]
    #extract the invoice details
    for i,row in enumerate(invoice.rows):
        invoice_dict[row[0]]=row[2]
    #clean up the date
    if "Fakturadato" in invoice_dict:
        formated_date:datetime
        formated_date=datetime.strptime(invoice_dict.get("Fakturadato"), "%d.%m.%Y").date()
        invoice_dict["Fakturadato"]=formated_date
    for i in range(len(checkitems.rows)-1):    #ignore the last row as this is just a summation of all the previous rows
        checkitem_list=checkitems.rows[i]
        list_length=len(checkitem_list)
        if list_length>1:
            lineitems.append(extract_check_items(checkitem_list))
        elif list_length==1:
            linked_workitem_list.append([i,checkitem_list[0]])
    invoice_dict['Lineitems']=lineitems
    return (invoice_dict,linked_workitem_list)

def update_line_item(start_index:int,end_index:int,line_items:Dict):
    tmp_index=0
    
    



def update_linked_items(linked_items:list,line_items:Dict):
    for linked_item in linked_items:
        print(linked_item)
        


invoice_index=7     #any invoice information will be at index 7 in the table_objects 
lineitems_index=9   #any lines items information will be at index 9 in the table_objects 
invoice={}
linked_items={}


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
 
#extract line items
invoice,linked_items=extract_invoice(table_objects[invoice_index],table_objects[lineitems_index])
update_linked_items(linked_items,invoice['Lineitems'])
