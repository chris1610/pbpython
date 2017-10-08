""" Example Dash application accompanying the post
at http://pbpython.com/plotly-dash-intro.html
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# Read in the Excel file
df = pd.read_excel(
    "https://github.com/chris1610/pbpython/blob/master/data/salesfunnel.xlsx?raw=True"
)

# Pivot the data to get it a summary format
pv = pd.pivot_table(
    df,
    index=['Name'],
    columns=["Status"],
    values=['Quantity'],
    aggfunc=sum,
    fill_value=0)

# Build a trace for each status that will eventual make the stacked bar
trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

# Create the basic app
app = dash.Dash()

# Populate the HTML structure of the app with the graph element
app.layout = html.Div(children=[
    html.H1(children='Sales Funnel Report'),
    html.Div(children='''National Sales Funnel Report.'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3, trace4],
            'layout':
            go.Layout(title='Order Status by Customer', barmode='stack')
        })
])

# Allow the app to serve from the command line
if __name__ == '__main__':
    app.run_server(debug=True)
