"""
Beer Analysis - Using Jupyter Code Cells
Accompanying article on https://pbpython.com/notebook-alternative.html
"""
# %%
import pandas as pd
import seaborn as sns
import plotly.express as px
# %%
# Load in the Craft Beer analysis
df_beers = pd.read_csv(
    'https://github.com/nickhould/craft-beers-dataset/blob/master/data/processed/beers.csv?raw=True',
    index_col=0)
df_breweries = pd.read_csv(
    'https://github.com/nickhould/craft-beers-dataset/blob/master/data/processed/breweries.csv?raw=True',
    index_col=0)
# %%
sns.set_style('whitegrid')

# %%
df_beers.head()

# %%
df_breweries.head()

# %%
df_beers.info()

# %%
df_breweries.info()

# %%
all_beer = pd.merge(df_beers,
                    df_breweries,
                    how='left',
                    left_on="brewery_id",
                    right_on="id",
                    suffixes=('_beer', '_brewery'))

# %%
all_beer.head()

# %%
# Useful to check for null values
empty_data = all_beer.isna().sum()

# %%
all_beer.info()

# %%
all_beer['ounces'].plot(kind='hist', title='Beer Size')

# %%
all_beer['IPA'] = all_beer['style'].str.contains('IPA', case=False)

# %%
all_beer['IPA'].value_counts()

# %%
all_beer_types = all_beer['style'].value_counts()

# %%
sns.catplot(data=all_beer, x='IPA', y='ibu', kind='box')

# %%
sns.catplot(data=all_beer, x='IPA', y='ibu', kind='swarm')

# %%
fig = px.scatter(all_beer, x="abv", y="ibu")
fig.show()

# %%
fig = px.scatter(all_beer,
                 x="abv",
                 y="ibu",
                 color='state',
                 hover_name='name_beer',
                 hover_data=['name_brewery'])
fig.show()

# %%
# Do some analysis on MN beers
mn_beer = all_beer[all_beer['state'].str.contains('MN')].copy()

# %%
all_beer['state'].value_counts()

# %%
all_beer.describe()

# %%
# Any relationship betwee alcohol volume and IBU?
fig = px.scatter(mn_beer,
                 x="abv",
                 y="ibu",
                 hover_name='name_beer',
                 hover_data=['name_brewery'])
fig.show()

# %%
