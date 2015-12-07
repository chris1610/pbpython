"""
See http://pbpython.com/advanced-excel-workbooks.html for details on this script

"""
from __future__ import print_function
import pandas as pd


def format_excel(writer):
    """ Add Excel specific formatting to the workbook
    """
    # Get the workbook and the summary sheet so we can add the formatting
    workbook = writer.book
    worksheet = writer.sheets['summary']
    # Add currency formatting and apply it
    money_fmt = workbook.add_format({'num_format': 42, 'align': 'center'})
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:C', 15, money_fmt)
    worksheet.add_table('A1:C22', {'columns': [{'header': 'account',
                                                'total_string': 'Total'},
                                               {'header': 'Total Sales',
                                                'total_function': 'sum'},
                                               {'header': 'Average Sales',
                                                'total_function': 'average'}],
                                   'autofilter': False,
                                   'total_row': True,
                                   'style': 'Table Style Medium 20'})


if __name__ == "__main__":
    sales_df = pd.read_excel('https://github.com/chris1610/pbpython/blob/master/data/sample-salesv3.xlsx?raw=true')
    sales_summary = sales_df.groupby(['name'])['ext price'].agg(['sum', 'mean'])
    # Reset the index for consistency when saving in Excel
    sales_summary.reset_index(inplace=True)
    writer = pd.ExcelWriter('sales_summary.xlsx', engine='xlsxwriter')
    sales_summary.to_excel(writer, 'summary', index=False)
    format_excel(writer)
    writer.save()
