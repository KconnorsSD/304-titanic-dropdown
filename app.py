######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/KconnorsSD/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Survivor']=df['Survived'].map({'Died':0, 'Made It':1})
df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list=['Sex', 'Fare', 'Age', 'Embarked']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
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
    grouped_mean=df.groupby(['Survivor', 'Cabin Class'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Died'].index,
        y=results.loc['Died'][continuous_var],
        name='Died',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Made It'].index,
        y=results.loc['Made It'][continuous_var],
        name='Made it',
        marker=dict(color=color2)
    )
    

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Survivor'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)