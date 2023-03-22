import plotly.graph_objects as go
import datetime as dt
import pandas as pd
from math import isnan


fig = go.Figure()

# Set axes properties
fig.update_xaxes(range=[dt.date(1936,1,1), dt.date(1940,1,1)], type="date")
fig.update_yaxes(range=[-1, 4.5])

focus_colors= {
    "politics": ("Gray", "Silver"),
    "economy": ("DarkOrange", "Orange"),
    "marine": ("RoyalBlue", "LightSkyBlue"),
    "military": ("DarkOliveGreen", "Olive")
}


source = pd.read_csv(r"C:\Users\Patryk\Desktop\Nowy folder\NSB_original.csv", encoding="utf-8")

previous_finish = dt.date(1936,1,1).isoformat()
day = dt.timedelta(days=1)

def get_original(key, value, source):
    for index, shape in source.iterrows():
        if shape[key] == value:
            return shape

for index, shape in source.iterrows():
    if shape["Resource"] == "POL_focus":
        source.at[index, "Start"] = previous_finish
        start = dt.date.fromisoformat(source.at[index, "Start"])
        duration = shape["Duration"] *  day
        finish = start + duration
        source.at[index, "Finish"] = finish.isoformat()
        previous_finish = source.at[index, "Finish"]
        
        fig.add_shape(type="rect",
                      xref="x",
                      yref="y",
                      x0=source.at[index, "Start"],
                      y0=2,
                      x1=source.at[index, "Finish"],
                      y1=4.5,
                      line=dict(
                          color=focus_colors[shape["Type"]][0],
                          width=3,
                          ),
                      fillcolor=focus_colors[shape["Type"]][1],
                      )

        fig.add_annotation(
            x=(start + (finish - start)/2).isoformat(),
            y=2,
            text=shape["Task"],
            showarrow=False,
            arrowhead=1,
            yshift=0,
            textangle=-90,
            yanchor="bottom",
            )


for index, shape in source.iterrows():
    if shape["Resource"] == "real":
        end_point= shape["Date"]
        fig.add_annotation(
            x=end_point,
            y=1,
            text=shape["Task"],
            showarrow=False,
            textangle=-90,
            yanchor="top",
            )
        parent = shape["Parent"];
        if type(parent) is str:
            original_task = get_original("Task", parent, source)
            print(parent)
            print(original_task)
            start_point = dt.date.fromisoformat(original_task["Finish"])
            end_point= shape["Date"]
            colors = focus_colors[original_task["Type"]]

            fig.add_shape(type="line",
                          x0=start_point,
                          y0=2,
                          x1=end_point,
                          y1=1,
                          line=dict(
                              color=colors[0],
                              width=4
                              )
                          )
     
fig.show()
