import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, path='/about')
df = px.data.gapminder()

layout = html.Div(
    [
        dcc.Markdown('# this will be the content of page about and much more')
    ]
)