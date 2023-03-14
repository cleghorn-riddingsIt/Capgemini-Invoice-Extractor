# Cap Invoice Extractor

## Summary
Takes a Cap invoice file and extracts the html into flat excel lines that can be poked into sharepoint
 
Each HTML file is structured in teh same manner and examples of these are shown in the Invoices folder

The data to extract from the html file has two aspects

### Charge Item
This is the hours booked by a consultant for a given week on a given work item. There may be many hours charged per work item. The work item is often not given until after the charge line in the html so the code will need to assume that any lines below a charge item are the work item(TP or remedy item) for the charges above. The properties of a charge item are:

- Summary: text(utf)
- Linked Work Item: text(utf)
- Consultant
  - First Name: string(utf)
  - Last Name: string(utf)
- Year: yera of the charge item(int)
- Week: week number for the year(int)
- Hours: Hours work in this charge item(float)
- Hourly rate: Hour rate in NOK
- taxRate: vat tax rate for this person

An example of the cell data for a charge item is
['026 RolesImplementation', 'RolesImplementation     Kumar, Ram 202306', '100491434 Gassco Forretningssupport', '29.21', 'HUR', '1409,00', '41156,89', '25%', '51446,11']

The resultant class maye look like this

Summary:RolesImplementation
Linked Work Item: Don't know yet. We would need to iterate to the next row to see if it has the above structure or not. If it doesn't it is most likely the Work Item
ConsultantFirstName:Ram
ConsultantLastName: Kumar
Year:2023
Week:06
HoursWorked:29.21
HourlyRate:1409.00  Note. We need to change the comma to a dec point
taxRate:25

All these charge items will be in row 9 of the table produced initially

### Invoice details
There will be multiple charge items per invoice
Fakturanummer	:	13200110114524  This is the Cap invoice number
Fakturadato	:	27.02.2023          This is when it was recieved
Ordrenummer	:	4500040156          This is the Gassco PO number

We then need a class with these properties and multiple charge Items

These items are in row 7 of the table.
