from datetime import datetime
from dash import Dash, dcc, html, Input, Output, callback
import requests
from bs4 import BeautifulSoup

app = Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('SendGrid status'),
        html.Div(id='status_time_count'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@callback(Output('status_time_count', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(count):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    try:
        URL = "https://status.sendgrid.com/#"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="page-status status-none")[0].find_all("span", class_="status font-large")[0].text
        results = "".join(line.strip() for line in results.split("\n"))
        status = results == "All Systems Operational"
    except:
        status = False

    if status:
        return [
            html.Span('🟢'),
            html.Span(current_time),
            html.Span('Requests: {0:.0f}'.format(count))
        ]
    else:
        return [
            html.Span('🔴'),
            html.Span(current_time),
            html.Span('Requests: {0:.0f}'.format(count))
        ]

if __name__ == '__main__':
    app.run()