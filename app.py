######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
#Added in Emerald Green for St Patricks Day
tabtitle = 'Chi Town!'
color1='#00C957'
color2='#FF0000'
color3='#7A67EE'
sourceurl = 'https://vck9grfshbi2or0.studio.us-east-2.sagemaker.aws/studiolab/default/jupyter/lab/tree/intuit-ga-dat15/projects/304-titanic-dropdown/app.py'
githublink = 'https://github.com/KconnorsSD/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv('Data/chicago2.csv')
df['Home Types']=df['HouseType'].map({'Condo':'Condominiums', 'Single-Family Home':'Single Family House', 'Multi-family Home':'Multi-Family Home'})
variables_list=['Price', 'CrimeIndex', 'MinutesToLoop', 'SchoolIndex', 'HouseSizeSqFt']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H1('Chicago housing data'),
    html.H2('Find your new home!'),
    html.H3('Check these options to get to know the Wicker Park area:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Home Types', 'Bath'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Condominiums'].index,
        y=results.loc['Condominiums'][continuous_var],
        name='Condominiums',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Single Family House'].index,
        y=results.loc['Single Family House'][continuous_var],
        name='Single Family House',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['Multi-Family Home'].index,
        y=results.loc['Multi-Family Home'][continuous_var],
        name='Multi-Family Home',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'HouseType'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)