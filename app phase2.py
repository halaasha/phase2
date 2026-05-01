from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("SuperMarket Analysis.csv")
df.columns = df.columns.str.strip()
df['Date'] = pd.to_datetime(df['Date'])
df['Sales'] = df['Sales'].astype(float)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Supermarket Sales Dashboard", style={'textAlign': 'center'}),
    html.Label("Select City:"),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': 'All', 'value': 'All'}] +
                [{'label': c, 'value': c} for c in df['City'].unique()],
        value='All'
    ),
    html.Label("Select Payment Method:"),
    dcc.Dropdown(
        id='payment-dropdown',
        options=[{'label': 'All', 'value': 'All'}] +
                [{'label': p, 'value': p} for p in df['Payment'].unique()],
        value='All'
    ),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('payment-dropdown', 'value')]
)
def update_graphs(city, payment):
    filtered = df.copy()
    if city != 'All':
        filtered = filtered[filtered['City'] == city]
    if payment != 'All':
        filtered = filtered[filtered['Payment'] == payment]

    daily = filtered.groupby('Date')['Sales'].sum().reset_index()
    line_fig = px.line(daily, x='Date', y='Sales',
                       title='Daily Sales Trend', markers=True)

    product = filtered.groupby('Product line')['Sales'].sum().reset_index()
    bar_fig = px.bar(product, x='Product line', y='Sales',
                     title='Sales by Product Line', color='Product line')

    return line_fig, bar_fig

server = app.server

if __name__ == '__main__':
    app.run(debug=True)
