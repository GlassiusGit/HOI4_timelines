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


fig = go.Figure()
fig.update_xaxes(range=[dt.date(1936,1,1), dt.date(1940,1,1)], type="date")
fig.update_yaxes(range=[-1, 4.5])


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
                  x0=start,
                  y0=2,
                  x1=end,
                  y1=4.5,
                  line=dict(
                      color=focus_colors[focus["Type"]][0],
                      width=3,
                      ),
                  fillcolor=focus_colors[focus["Type"]][1],
                  )

    fig.add_annotation(
        x=(start + (end - start)/2).isoformat(),
        y=2,
        text=focus["Focus"],
        showarrow=False,
        arrowhead=1,
        yshift=0,
        textangle=-90,
        yanchor="bottom",
        )

# real events
reals = pd.read_csv(r"C:\Users\Patryk\Desktop\Nowy folder\real_events.csv")

for index, event in reals.iterrows():
    end_point= event["Date"]
    fig.add_annotation(
        x=end_point,
        y=1,
        text=event["Event"],
        showarrow=False,
        textangle=-90,
        yanchor="top",
        )
    parents = event["Focuses"];
    if type(parents) is str:
        for parent in parents.split(';'):
            original_task = get_original("Focus", parent, NSB)
            start_point = original_task["End"]
            end_point= event["Date"]
            colors = event["Type"]

            fig.add_shape(type="line",
                          x0=start_point,
                          y0=2,
                          x1=end_point,
                          y1=1,
                          line=dict(
                              color=focus_colors[event["Type"]][0],
                              width=4
                              )
                          )
     
fig.show()
