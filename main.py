from bs4 import BeautifulSoup
from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict
from datetime import datetime
from typing import Dict
from typing import List


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


class Table:
    def __init__(self, caption: str, rows: List[List[str]]):
        self.caption = caption
        self.rows = rows
        
class Consultant:
     def __init__(self, firstname='', lastname=''):
         self._firstname=firstname
         self._lastname=lastname

class LineItem:
    _summary:str
    _linked_item:str
    _hours:float
    _rate:float
    _tax_rate:float
    _totalgross:float
    _consultant=Consultant
    
    def __init__(self, summary='', linked_item='', hours:float=0, rate:float=0, tax_rate:float=0,total_gross:float=0,consultant:Consultant=None):
        self._summary = summary
        self._linked_item = linked_item
        self._hours = hours
        self._rate = rate
        self._tax_rate = tax_rate
        self._totalgross=total_gross
        self._consultant=consultant
        
    
    def convert_to_float(self,value: str) -> float:
        try:
            cleaned_string = value.replace(",", ".").replace("%", "")
            return float(cleaned_string)
        except ValueError:
            raise ValueError(f"{value} is not a valid float")
       
    
    @property
    def hours(self):
        return self._hours
    @hours.setter
    def hours(self, value):
        self._hours = convert_to_float(value)
    @property
    def rate(self):
        return self._rate
    @hours.setter
    def hours(self, value):
        self._rate = convert_to_float(value)
    @property
    def taxrate(self):
        return self._taxrate
    @hours.setter
    def hours(self, value):
        self._taxrate = convert_to_float(value)
    @property
    def totalgross(self):
        return self._totalgross
    @hours.setter
    def hours(self, value):
        self._totalgross = convert_to_float(value)
        
class Invoice:
    _invoice_number:str
    _invoice_date:datetime
    _po_number:str
    _po_reference:str
    _customer_number:str
    _line_items:List[LineItem]
    def __init__(self, invoice_number='', invoice_date:datetime=None, po_number='', po_reference='', customer_number='',line_items=None):
        self._invoice_number = invoice_number
        self._invoice_date = invoice_date
        self._po_number = po_number
        self._po_reference= po_reference
        self._customer_number = customer_number
        self._line_items=line_items
        
    @property
    def invoice_date(self):
        return self._invoice_date
    @invoice_date.setter
    def hours(self, value):
        self._invoice_date = datetime.strptime(value, "%d.%m.%Y").date()
        

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

def update_line_item(start_index:int,end_index:int,linked_item:str, line_items:Dict):
    tmp_index=0
    
    



def update_linked_items(linked_items:list,line_items:Dict):
    for linked_item in linked_items:
        stop_index=int(linked_item[0])
        linked_item_text=str(linked_item[1])
        


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
