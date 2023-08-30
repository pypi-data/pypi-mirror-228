import glob, os
import pandas as pd
from fpdf import FPDF, XPos, YPos
from pathlib import Path

# * * * * * * *   G L O B A L   V A R I A B L E S   * * * * * * * #
WORKING_DIR = '/Volumes/EVO1T/OneDrive/Tutorials/2.Active/Learn Python in 50 Days/Apps/App04/'


# * * * * * * * * * * *  F U N C T I O N S   * * * * * * * * * * * #


# set the working directory
def setWorkingDirectory(root_path:str=WORKING_DIR):
    os.chdir(root_path)

def generate(
        invoices_path:str='invoices/to_process', 
        pdf_path:str='invoices/to_process',
        image_path_name:str='images/pythonhow.png',
        product_id:str='product_id',
        product_name:str='product_name',
        amount:str='amount_purchased',
        unit_price:str='price_per_unit',
        total_price:str='total_price'
    ):
    invoices_path = invoices_path[:-1] if invoices_path[-1] == '/' else  invoices_path # remove trailling '/'
    pdf_path = pdf_path[:-1] if pdf_path[-1] == '/' else  pdf_path # remove trailling '/'

    filepaths = glob.glob(f'{invoices_path}/*.xlsx')

    for filepath in filepaths:
        print(f'Processing file {filepath} ...')

        # load the excel file to DF
        df = pd.read_excel(filepath, sheet_name='Sheet 1')
        grand_total = 0.0
        
        # add it to a PDF document
        '''  **** layout ****
            Invoice #: <invoice_number>
            Date: <date>

            [Table]
            [header] Product ID  Product Name    Amount  Unit Price  Tatal Price
            [lines]  <prod.._id> <prod.._name>   <am..>  <price_..>  <am..> * <price_..>


            The total amount is <grand_total> Euros.
            PythonHow <logo>
        '''
        # get invoice numner and date and set pdf_filename
        filename = Path(filepath).stem
        inv_number = filename.split('-')[0]
        inv_date = filename.split('-')[1].replace('.', '-')
        pdf_filename = f'{pdf_path}/{filename}.pdf'

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        pdf.set_font(family='Arial', size=16, style='B')
        pdf.cell(h=8, txt=f'Invoice Number: ', align='L')

        pdf.set_font(family='Arial', size=16, style='')
        pdf.cell(h=8, txt=f'{inv_number}', align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(family='Arial', size=16, style='B')
        pdf.cell(txt=f'Invoice Date: ', align='L')

        pdf.set_font(family='Arial', size=16, style='')
        pdf.cell(txt=f'{inv_date}', align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.cell(h=16, txt=f' ', align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # *** write the table
        # write the header
        #labels = [ x.replace('_', ' ').title() for x in df.columns]
        pdf.set_font(family='Arial', size=14, style='B')
        pdf.cell(w=34, h=8, txt='Product ID', align='L', border=1)
        pdf.cell(w=58, h=8, txt='Product Name', align='L', border=1)
        pdf.cell(w=28, h=8, txt='Amount', align='L', border=1)
        pdf.cell(w=33, h=8, txt='Unit Price', align='L', border=1)
        pdf.cell(w=36, h=8, txt='Total Price', align='L', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # write the invoice lines
        for i, row in df.iterrows():
            pdf.set_font(family='Arial', size=12, style='')
            pdf.cell(w=34, h=8, txt=f" {row[product_id]}", align='L', border=1)
            pdf.cell(w=58, h=8, txt=f" {row[product_name]}", align='L', border=1)
            pdf.cell(w=28, h=8, txt=f" {row[amount]}", align='R', border=1)
            pdf.cell(w=33, h=8, txt=f" {row[unit_price]:.2f}", align='R', border=1)
            pdf.cell(w=36, h=8, txt=f" {row[total_price]:.2f}", align='R', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            grand_total += float(row[total_price])

        # write the grand total
        pdf.set_font(family='Arial', size=14, style='B')
        pdf.cell(w=(34+58+28), h=8, txt='', align='L', border=0)
        pdf.cell(w=33, h=8, txt='Grand Total: ', align='R', border=0)
        pdf.cell(w=36, h=8, txt=f" {grand_total:.2f}", align='R', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.cell(h=16, txt=f' ', align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # add footer
        pdf.set_font(family='Arial', size=12, style='')
        pdf.cell(h=8, txt='The total price is: ', align='L', border=0)
        pdf.cell(h=8, txt=f"{grand_total:.2f}", align='L', border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font(family='Arial', size=14, style='B')
        pdf.cell(w=33, h=12, txt='PythonHow', align='L', border=0)
        pdf.image(image_path_name, w=10)

        # write the file
        os.makedirs(pdf_path, exist_ok=True)
        pdf.output(pdf_filename)

        print(df, '\n\n')


# * * * * * * * * * * * * *  M  A  I  N  * * * * * * * * * * * * * #

