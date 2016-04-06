import pandas as pd
from sqlalchemy import create_engine
from xlwings import Workbook, Range
import os


def summarize_sales():
    """
    Retrieve the account number and date ranges from the Excel sheet
    Read in the data from the sqlite database, then manipulate and return it to excel
    """
    # Make a connection to the calling Excel file
    wb = Workbook.caller()

    # Connect to sqlite db
    db_file = os.path.join(os.path.dirname(wb.fullname), 'pbp_proj.db')
    engine = create_engine(r"sqlite:///{}".format(db_file))

    # Retrieve the account number from the excel sheet as an int
    account = Range('B2').options(numbers=int).value

    # Get our dates - in real life would need to do some error checking to ensure
    # the correct format
    start_date = Range('D2').value
    end_date = Range('F2').value

    # Clear existing data
    Range('A5:F100').clear_contents()

    # Create SQL query
    sql = 'SELECT * from sales WHERE account="{}" AND date BETWEEN "{}" AND "{}"'.format(account, start_date, end_date)

    # Read query directly into a dataframe
    sales_data = pd.read_sql(sql, engine)

    # Analyze the data however we want
    summary = sales_data.groupby(["sku"])["quantity", "ext-price"].sum()

    total_sales = sales_data["ext-price"].sum()

    # Output the results
    if summary.empty:
        Range('A5').value = "No Data for account {}".format(account)
    else:
        Range('A5').options(index=True).value = summary
        Range('E5').value = "Total Sales"
        Range('F5').value = total_sales
