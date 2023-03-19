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

def checkInt(int_string:str)->float:
    #takes a string parameter and returns the integer convertion or -1 if the string isn't value
    cleaned_string=int_string.replace(",",".").replace("%","")# remove any comma's or % and replace with decimal points
    result_float=-1.0
    try:
        result_float=float(cleaned_string)     
    except ValueError:
        print(f"{cleaned_string} is not a valid float")
    return result_float


def extractCheckItems(row:list):
#expect the row object to have the following structure
#['026 RolesImplementation', 'RolesImplementation     Kumar, Ram 202306', '100491434 Gassco Forretningssupport', '29.21', 'HUR', '1409,00', '41156,89', '25%', '51446,11']
    check_items_row={}
    consultant_details=str(row[1]).split()
    check_items_row['summary']=consultant_details[0]
    check_items_row['hours']=checkInt(row[3])
    check_items_row['rate']=checkInt(row[5])
    check_items_row['totalnet']=checkInt(row[6])
    check_items_row['taxrate']=checkInt(row[7])
    check_items_row['totalgross']=checkInt(row[7])
    
    
        
    #column 2 contains bothe the consultant name and the week/year so this needs to be extracted
   
    print(row)
    return check_items_row
    
    


def extract_invoice(invoice:Table,checkitems:Table)->Dict:
    invoice_dict={}
    checkitems_dict={}
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
        linked_work_item=""
        if list_length>1:
            checkitems_dict=extractCheckItems(checkitem_list)
        elif list_length==1:
            linked_work_item=checkitem_list[0]
            saved_index=i   #store where you where when the linked_work_item wa last applied
            #at this point we need to iterate through the extractCheckItems that exist and add the linked_work_item field
        invoice_dict['lineitems'+str(i)]=checkitems_dict
    return invoice_dict

invoice_index=7     #any invoice information will be at index 7 in the table_objects 
lineitems_index=9   #any lines items information will be at index 9 in the table_objects 
invoice={}
check_items={}


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
invoice=extract_invoice(table_objects[invoice_index],table_objects[lineitems_index])

print(table_objects)