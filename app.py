######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Chi Town!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://vck9grfshbi2or0.studio.us-east-2.sagemaker.aws/studiolab/default/jupyter/lab/tree/intuit-ga-dat15/projects/304-titanic-dropdown/app.py'
githublink = 'https://github.com/KconnorsSD/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv('Data/chicago2.csv')
df['Baths']=df['Bath'].map({2:'two', 3:'three', 4:'four'})
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
    html.H3('Choose a continuous variable for summary statistics:'),
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
    grouped_mean=df.groupby(['Baths', 'HouseType'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['two'].index,
        y=results.loc['two'][continuous_var],
        name='Two Baths',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['three'].index,
        y=results.loc['three'][continuous_var],
        name='Three Baths',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['four'].index,
        y=results.loc['four'][continuous_var],
        name='Four Baths',
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