""" Interactive Wine Visualization Tool

See pbpython.com for the associated blog post explaining the process and
goals of this script
"""

import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache


# Define a cached function to read in the CSV file and return a dataframe
@lru_cache()
def load_data():
    df = pd.read_csv("Aussie_Wines_Plotting.csv", index_col=0)
    return df

# Column order for displaying the details of a specific review
col_order = ["price", "points", "variety", "province", "description"]

all_provinces = [
    "All", "South Australia", "Victoria", "Western Australia",
    "Australia Other", "New South Wales", "Tasmania"
]

# Setup the display portions including widgets as well as text and HTML
desc = Div(text="All Provinces", width=800)
province = Select(title="Province", options=all_provinces, value="All")
price_max = Slider(start=0, end=900, step=5, value=200, title="Maximum Price")
title = TextInput(title="Title Contains")
details = Div(text="Selection Details:", width=800)

# Populate the data with the dataframe
source = ColumnDataSource(data=load_data())

# Build out the hover tools
hover = HoverTool(tooltips=[
    ("title", "@title"),
    ("variety", "@variety"),
])

# Define the tool list as a list of the objects so it is easier to customize
# each object
TOOLS = [
    hover, BoxZoomTool(), LassoSelectTool(), WheelZoomTool(), PanTool(),
    ResetTool(), SaveTool()
]

# Build out the figure with the individual circle plots
p = figure(
    plot_height=600,
    plot_width=700,
    title="Australian Wine Analysis",
    tools=TOOLS,
    x_axis_label="points",
    y_axis_label="price (USD)",
    toolbar_location="above")

p.circle(
    y="price",
    x="points",
    source=source,
    color="variety_color",
    size=7,
    alpha=0.4)


# Define the functions to update the data based on a selection or change

def select_reviews():
    """ Use the current selections to determine which filters to apply to the
    data. Return a dataframe of the selected data
    """
    df = load_data()

    # Determine what has been selected for each widgetd
    max_price = price_max.value
    province_val = province.value
    title_val = title.value

    # Filter by price and province
    if province_val == "All":
        selected = df[df.price <= max_price]
    else:
        selected = df[(df.province == province_val) & (df.price <= max_price)]

    # Further filter by string in title if it is provided
    if title_val != "":
        selected = selected[selected.title.str.contains(title_val) == True]

    # Example showing how to update the description
    desc.text = "Province: {} and Price < {}".format(province_val, max_price)
    return selected


def update():
    """ Get the selected data and update the data in the source
    """
    df_active = select_reviews()
    source.data = ColumnDataSource(data=df_active).data


def selection_change(attrname, old, new):
    """ Function will be called when the poly select (or other selection tool)
    is used. Determine which items are selected and show the details below
    the graph
    """
    selected = source.selected["1d"]["indices"]

    # Need to get a list of the active reviews so the indices will match up
    df_active = select_reviews()

    # If something is selected, then get those details and format the results
    # as an HTML table
    if selected:
        data = df_active.iloc[selected, :]
        temp = data.set_index("title").T.reindex(index=col_order)
        details.text = temp.style.render()
    else:
        details.text = "Selection Details"


# Setup functions for each control so that changes will be captured and data
# updated as required
controls = [province, price_max, title]

for control in controls:
    control.on_change("value", lambda attr, old, new: update())

# If the source is changed to a selection, execute that selection process
source.on_change("selected", selection_change)

# The final portion is to layout the parts and get the server going

# Build a box for all the controls
inputs = widgetbox(*controls, sizing_mode="fixed")

# Define a simple layout
l = layout([[desc], [inputs, p], [details]], sizing_mode="fixed")

# Update the data and instantiate the service
update()
curdoc().add_root(l)

# Show the title in the browser bar
curdoc().title = "Australian Wine Analysis"
