import plotly.graph_objects as go
import datetime as dt
import pandas as pd
from math import isnan

def get_original(key, value, source):
    for index, shape in source.iterrows():
        if shape[key] == value:
            return shape


def populate_dates(starting_date, df):
    current_date = dt.date.fromisoformat(starting_date)
    for index, focus in df.iterrows():
        df.at[index, "Start"] = current_date
        delta = df.at[index, "Duration"] * dt.timedelta(days=1)
        current_date += delta
        df.at[index, "End"] = current_date

orig_x0=0
orig_x1=1
real_x0=2

fig = go.Figure()
fig.update_xaxes(
    range=[-1, 3.5],
    showgrid=False
    )
    
fig.update_yaxes(
    range=[dt.date(1940,1,1), dt.date(1936,1,1)],
    type="date",
    #autorange="reversed",
    showgrid=False
    )


focus_colors= {
    "politics": ("Gray", "Silver"),
    "economy": ("DarkOrange", "Orange"),
    "marine": ("RoyalBlue", "LightSkyBlue"),
    "military": ("DarkOliveGreen", "Olive")
}

# NSB data
NSB = pd.read_csv(r"C:\Users\Patryk\Desktop\Nowy folder\NSB_original.csv", encoding="utf-8")
populate_dates('1936-01-01', NSB)
        

for index, focus in NSB.iterrows():
    start = NSB.at[index, "Start"]
    end = NSB.at[index, "End"]
    fig.add_shape(type="rect",
                  xref="x",
                  yref="y",
                  x0=orig_x0,
                  y0=start,
                  x1=orig_x1,
                  y1=end,
                  line=dict(
                      color=focus_colors[focus["Type"]][0],
                      width=3,
                      ),
                  fillcolor=focus_colors[focus["Type"]][1],
                  layer="below"
                  )
    fig.add_trace(go.Scatter(
        y=[(start + (end - start)/2).isoformat()],
        x=[orig_x0 + (orig_x1 - orig_x0)/2],
        text=NSB.at[index, "Focus"],
        mode="text",
        hovertext=NSB.at[index, "Hovertext"],
        #textposition="left",
        showlegend=False
                  ))

# real events
reals = pd.read_csv(r"C:\Users\Patryk\Desktop\Nowy folder\real_events.csv")

for index, event in reals.iterrows():
    end_point= event["Date"]
    fig.add_trace(go.Scatter(
        y=[end_point],
        x=[real_x0],
        text=event["Event"],
        mode="text",
        hovertext=reals.at[index, "Hovertext"],
        showlegend=False,
        textposition="middle right",
        ))
    parents = event["Focuses"];
    if type(parents) is str:
        for parent in parents.split(';'):
            original_task = get_original("Focus", parent, NSB)
            start_point = original_task["End"]
            end_point= event["Date"]
            colors = event["Type"]

            fig.add_shape(type="line",
                          x0=orig_x1,
                          y0=start_point,
                          x1=real_x0,
                          y1=end_point,
                          line=dict(
                              color=focus_colors[event["Type"]][0],
                              width=4
                              )
                          )
     
fig.show()
