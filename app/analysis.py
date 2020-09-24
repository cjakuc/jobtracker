import plotly
import plotly.graph_objects as go
import json

def num_apps(jobs):
    date_dict = {}
    for job in jobs:
        if job.date_added not in date_dict:
            date_dict[job.date_added.strftime('%Y-%m-%d')] = 1
        else:
            date_dict[job.date_added.strftime('%Y-%m-%d')] += 1

    x = list(date_dict.keys())
    y = list(date_dict.values())

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = x,
        y = y
    ))

    fig.update_layout(
        title = {'text': "Number of Applications Over Time",
                 'y':0.9,
                 'x':0.5,
                 'xanchor': 'center',
                 'yanchor': 'top'},
        xaxis_title = "Date",
        yaxis_title = "Number of Applications",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(step="all"),
                    dict(count=7, label="1 Week", step="day", stepmode="backward"),
                    dict(count=1, label="1 Month", step="month", stepmode="backward")
                ])
            )
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def num_status(jobs):
    status_dict = {}
    for job in jobs:
        if job.status not in status_dict:
            status_dict[job.status] = 1
        else:
            status_dict[job.status] += 1

    x = list(status_dict.keys())
    y = list(status_dict.values())

    print(x)
    print(y)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = x,
        y = y,
        # width = [2 for i in x],
        width = .15
    ))

    fig.update_layout(
        title = {'text': "Number of Applications per Status",
                 'y':0.9,
                 'x':0.5,
                 'xanchor': 'center',
                 'yanchor': 'top'},
        xaxis_title = "Status",
        yaxis_title = "Number of Applications",
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON