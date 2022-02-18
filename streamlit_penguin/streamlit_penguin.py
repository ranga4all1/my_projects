# ### Streamlit visualization app - Palmer Archipelago (Antarctica) penguin data
# 
# To perform visualization with streamlit we’re using a dataset of penguins. The dataset can be downloaded by using the following
# [link:](https://www.kaggle.com/parulpandey/palmer-archipelago-antarctica-penguin-data?select=penguins_size.csv)

#  import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from bokeh.plotting import figure
import altair as alt

# load the data
df = pd.read_csv("penguins_size.csv")
# print(df)
# print("\n")
# print(df.head())

# df.columns
# df.info()

# check for missing values in the data
# df.isnull().sum()

# remove the missing values and save dataframe as a new dataframe variable new_df
new_df = df.dropna()
# print(new_df)

# ### scatterplot with widgets using Streamlit
#
# Let’s plot an interesting scatter plotting by choosing the different categories from the penguin's dataset.
# The following code will help to make a scatter plot by selecting several species of penguins and picking
# categories for the x-axis and y-axis from culmen length, culmen depth, flipper length, and body mass.

# scatterplot with widgets using Streamlit

st.subheader('Streamlit visualization app - Palmer Archipelago (Antarctica) penguin data - Scatter plotting with selection of category')

# select box is a Displayed widget that allows the user to select a value from a list of options.
select_species = st.selectbox('Select species', new_df['species'].unique())
selected_x_variable = st.selectbox('Select x-axis variable', new_df.columns[2:6])
selected_y_variable = st.selectbox('Select y-axis variable', new_df.columns[2:6])

p_df = new_df[new_df['species'] == select_species]
fig, ax = plt.subplots()
ax = plt.scatter(x = p_df[selected_x_variable], y = p_df[selected_y_variable])
plt.xlabel(selected_x_variable)
plt.ylabel(selected_y_variable)
st.pyplot(fig)

#### Now, let's visualize additional supporting data using Streamlit

# st.write will help us to write the data in application and head() will show the first 5 rows of the data
st.title("First 5 rows of 'Penguin Size' dataset")
st.write(new_df.head())

# #### Let's start plotting the data
# 
# Plot a Line chart, Bar chart, and Area chart with Streamlit.
# 
# To plot the Line chart, Area chart, and Bar chart by using the Streamlit, use the following code. it will help to plot
# the flipper length and bill length of penguins.

st.title('Streamlit Line_chart, Bar_chart and Area_chart')
df_dbh_grouped = pd.DataFrame(new_df.groupby(['flipper_length_mm']).count()['culmen_length_mm'],)
df_dbh_grouped.columns = ["flipper and culmen length"]
# print(df_dbh_grouped)

# to draw line chart
st.subheader('Line_chart')
st.line_chart(df_dbh_grouped)

# to draw bar chart
st.subheader('Bar_chart')
st.bar_chart(df_dbh_grouped)

# to draw area chart
st.subheader('Area_chart')
st.area_chart(df_dbh_grouped)


# #### Plotting with the help of Seaborn and Matplotlib
# 
# We can also use `matplotlib` and `seaborn` libraries for plotting with stramlit. The following code will help to
# plot a `histogram` of penguin’s **flipper length**.:

st.title("Seaborn and Matplotlib Histograms")

# Making Seaborn chart
st.subheader("Seaborn chart")
fig_sb, ax_sb = plt.subplots()
ax_sb = sns.histplot(new_df['flipper_length_mm'], kde=False, bins=30)
plt.xlabel('flipper_length_mm')
plt.ylabel('count')
st.pyplot(fig_sb)

# Making matplotlib chart
st.subheader("Matplotlib chart")
fig_mp, ax_mp = plt.subplots()
ax_mp.hist(new_df['flipper_length_mm'], bins=30)
plt.xlabel('flipper_length_mm')
plt.ylabel('count')
st.pyplot(fig_mp)

# #### Plotly
# 
# Plotly is an open-source library that provides a list of chart types as well as tools with callbacks to make a
# dashboard. Let’s use Plotly to visualize our data. Import the Plotly library, and then we’ll use the following code
# to plot the `histogram`:

# create plotly histogram

st.title("Plotly Histogram - Penguins")
fig = px.histogram(new_df, x="body_mass_g", nbins=30)
st.plotly_chart(fig)

# #### Bokeh
# 
# Bokeh is a Python data visualization library that generates fast interactive charts and plots. Let’s use the bokeh
# library to create a `scatter` plot, as shown below:

# create bokeh plots in streamlit
st.title("Bokeh plots - Penguins")
st.subheader("Bokeh chart")
scatterplot = figure(title="Bokeh Scatterplot")
scatterplot.scatter(new_df['culmen_length_mm'], new_df['culmen_depth_mm'])
scatterplot.xaxis.axis_label = 'culmen_depth_mm'
scatterplot.yaxis.axis_label = 'culmen_length_mm'
st.bokeh_chart(scatterplot)

# #### ALtair
# 
# Altair is a Vega-Lite Python interface that allows you to specify Vega-Lite charts in Python. Using the Altair
# library, the following code will assist you in creating a bar chart:

#  create altair bar chart

st.title("Altair Bar Chart - Penguins")
st.subheader("Altair Bar Chart")
fig = alt.Chart(new_df).mark_bar().encode(x = 'species', y = 'body_mass_g').properties(width=600, height=400)

st.altair_chart(fig)

# run this app via terminal using below command
# streamlit run streamlit_penguins.py