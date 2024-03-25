#!/usr/bin/env python
# coding: utf-8

# In[12]:


# Importing required libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# In[13]:


# Reading the data from IBM Cloud
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')


# In[14]:


# Initialize the Dash app
app = dash.Dash(__name__)

# Giving the Dash app a title
app.title = "Automobile Statistics Dashboard"


# In[15]:


# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Creating the dropdown menu options
dropdown_options = [
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},      
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ]


# In[16]:


# Create the layout of the app

app.layout = html.Div([
    # Title 
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36',
            'font-size': '24px'}
    ),
   
    html.Div([#Adding two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            value='Select Statistics',
            style={'width': '80%', 'padding': '3px',
            'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),

    # Dropdown for year selection
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            style={'width': '80%', 'padding': '3px',
                'fontSize': '20px', 'textAlignLast': 'center'}),
        html.Div([
            html.Div(id='output-container', className='chart-grid',
            style={'display': 'flex'}),
        ]),])
])


# In[17]:


# Creating Callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        


# Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                        x='Year',
                        y='Automobile_Sales',
                        title="Automobile Sales Fluctuation Over Recession Period")
        )


# The average number of vehicles sold by vehicle type       
        sales_rec = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(sales_rec, 
                        x='Vehicle_Type', 
                        y='Automobile_Sales',
                        title="Average Vehicles Sold by Vehicle Type During Recession")
        )

        
# Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                        values='Advertising_Expenditure', 
                        names='Vehicle_Type',
                        title="Expenditure Share by Vehicle Type During Recession")
        )


# Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_rec = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_rec, 
                        x='Vehicle_Type', 
                        y='unemployment_rate',
                        title="Effect of Unemployment Rate on Vehicle Type During Recession")
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(R_chart4)])
            ]

# Creating and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              
# Creating Graphs Yearly data
                              
# Yearly Automobile sales using a line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year',
                y='Automobile_Sales', title='Yearly Automobile sales'))
            
# Total Monthly Automobile sales using a line chart.
        mas = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month',
                y='Automobile_Sales', title='Monthly Automobile sales'))

# Bar chart for the average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph( figure=px.bar(avr_vdata, x='Vehicle_Type', color='Vehicle_Type',
                y='Automobile_Sales',title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

# Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(figure =px.bar(exp_data, x='Vehicle_Type', color='Vehicle_Type',
                    y='Advertising_Expenditure', title='Advertisement Expenditure for each vehicle'))

#T Returning the graphs for displaying Yearly data
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)]),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)])
                ]
        
    else:
        return None




# In[18]:


# Running the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

