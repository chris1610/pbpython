# -*- coding: utf-8 -*-
"""
Simple Pandas program to combine Excel files and summarize data.
See http://pbpython.com/pandas-gui.html for details on this script
This demonstrates the use of Gooey to add a simple UI on top of the script
"""
from __future__ import print_function
import pandas as pd
import numpy as np
import glob
import os
import json
from gooey import Gooey, GooeyParser


@Gooey(program_name="Create Quarterly Marketing Report")
def parse_args():
    """ Use GooeyParser to build up the arguments we will use in our script
    Save the arguments in a default json file so that we can retrieve them
    every time we run the script.
    """
    stored_args = {}
    # get the script name without the extension & use it to build up
    # the json filename
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    # Read in the prior arguments as a dictionary
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)
    parser = GooeyParser(description='Create Quarterly Marketing Report')
    parser.add_argument('data_directory',
                        action='store',
                        default=stored_args.get('data_directory'),
                        widget='DirChooser',
                        help="Source directory that contains Excel files")
    parser.add_argument('output_directory',
                        action='store',
                        widget='DirChooser',
                        default=stored_args.get('output_directory'),
                        help="Output directory to save summary report")
    parser.add_argument('cust_file',
                        action='store',
                        default=stored_args.get('cust_file'),
                        widget='FileChooser',
                        help='Customer Account Status File')
    parser.add_argument('-d', help='Start date to include',
                        default=stored_args.get('d'),
                        widget='DateChooser')
    args = parser.parse_args()
    # Store the values of the arguments so we have them next time we run
    with open(args_file, 'w') as data_file:
        # Using vars(args) returns the data as a dictionary
        json.dump(vars(args), data_file)
    return args


def combine_files(src_directory):
    """ Read in all of the sales xlsx files and combine into 1
    combined DataFrame
    """
    all_data = pd.DataFrame()
    for f in glob.glob(os.path.join(src_directory, "sales-*.xlsx")):
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True)
    all_data['date'] = pd.to_datetime(all_data['date'])
    return all_data


def add_customer_status(sales_data, customer_file):
    """ Read in the customer file and combine with the sales data
    Return the customer with their status as an ordered category
    """
    df = pd.read_excel(customer_file)
    all_data = pd.merge(sales_data, df, how='left')
    # Default everyone to bronze if no data included
    all_data['status'].fillna('bronze', inplace=True)
    # Convert the status to a category and order it
    all_data["status"] = all_data["status"].astype("category")
    all_data["status"].cat.set_categories(["gold", "silver", "bronze"], inplace=True)
    return all_data


def save_results(sales_data, output):
    """ Perform a summary of the data and save the data as an excel file
    """
    summarized_sales = sales_data.groupby(["status"])["unit price"].agg([np.mean])
    output_file = os.path.join(output, "sales-report.xlsx")
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    summarized_sales = summarized_sales.reset_index()
    summarized_sales.to_excel(writer)


if __name__ == '__main__':
    conf = parse_args()
    print("Reading sales files")
    sales_df = combine_files(conf.data_directory)
    print("Reading customer data and combining with sales")
    customer_status_sales = add_customer_status(sales_df, conf.cust_file)
    print("Saving sales and customer summary data")
    save_results(customer_status_sales, conf.output_directory)
    print("Done")
