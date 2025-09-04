from dash import Dash, html,dcc
from dash.dependencies import Input, Output
import requests ,json

import plotly.graph_objs as go

import requests

def get_wheather():
    lat, lon = 28.61, 77.21
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(url).json()
    hourly = response.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    humidity = hourly.get("relative_humidity_2m", [])
    wind_speed = hourly.get("wind_speed_10m", [])
    
    return times,temps  # First 12 hours



    

app = Dash()

app.layout = html.Div([
    html.H1("Weather of Delhi"),
    html.Button("Get Weather" , id ="button"),
    dcc.Graph(
        id="temp-graph"
    )
])

@app.callback(
    Output("temp-graph" ,"figure"),
    Input("button", "n_clicks")
)
def update(n_clicks):
    if n_clicks:
        times, temp = get_wheather()
        figure = {
            "data" :[
                go.Scatter(x = times , y= temp , mode="lines+markers")
            ],
            "layout" :{
                "title": {"text": "Temperature of Delhi for Next 12 Hours"},
                "xaxis": {"title": {"text":"Time"}},
                "yaxis": {"title":{"text": "Temperature (°C)"}}
            }
        }
        return figure
    return {
        "data" :[],
        "layout":{"title": {"text": "Temperature of Delhi for Next 12 Hours"},}
    }

# app.layout = html.Div([
#     html.Button("Click me", id="my-button"),
#     html.Div(id="output-text")
# ])

# @app.callback(
#     Output("output-text", "children"),
#     Input("my-button", "n_clicks")
# )
# def update_text(n_clicks):
#     if n_clicks:
#         return f"Button clicked {n_clicks} times!"
#     return "Button not clicked yet."

if __name__ == '__main__':
    app.run(debug=True)
