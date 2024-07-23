# import pandas as pd
# from dash import Dash, dcc, html
# import plotly.express as px
# from plotly.subplots import make_subplots
# import requests
# import datetime

# from dash.dependencies import Input, Output, State

# # Initialize the app
# app = Dash(__name__)

# # Navbar definition
# navbar = html.Nav([
#     html.Div([
#         html.Strong("ESG", style={"font-weight": "bold", "font-size": "20px", "color": "white", "margin-right": "20px"}),
#         html.Ul([
#             html.Li(html.A("Home", href="/", style={"color": "white"})),
#             html.Li(html.A("About", href="/about", style={"color": "white"})),
#             html.Li(html.A("Contact", href="/contact", style={"color": "white"}))
#         ], style={"list-style": "none", "display": "flex", "padding": 0, "margin": 0})
#     ], style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "50px"})
# ], style={"background-color": "blue", "padding": "10px"})

# # App layout
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     navbar,
#     html.Div(id='page-content'),
#     html.Hr(),
# ])

# # Define a callback to update the page content based on the URL
# @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/about':
#         return html.Div([
#             html.H2("About Page"),
#             html.P("This is the About page content.")
#         ])
#     elif pathname == '/contact':
#         return html.Div([
#             html.H2("Contact Page"),
#             html.P("This is the Contact page content.")
#         ])
#     else:
#         return html.Div([
#             html.H2("Home Page"),
#             html.P("This is the Home page content.")
#         ])

# if __name__ == '__main__':
#     app.run_server(debug=True)
