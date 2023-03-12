import plotly.graph_objects as go
import datetime as dt


fig = go.Figure()

'''
# Create scatter trace of text labels
fig.add_trace(go.Scatter(
    x=[1.5, 3],
    y=[2.5, 2.5],
    text=["Rectangle reference to the plot",
          "Rectangle reference to the axes"],
    mode="text",
))
'''

# Set axes properties
fig.update_xaxes(range=[dt.date(1936,1,1), dt.date(1940,1,1)], type="date")
fig.update_yaxes(range=[0, 4])

focus_colors= {
    "politics": ("RoyalBlue", "LightSkyBlue")
}


source = [
    dict(Resource="POL_focus",  Task="The Castle",                      Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Dissolve the Sejm",               Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Maintain the Dictatorship",       Duration=35,    Type="politics"),
    dict(Resource="real",       Task="Powołanie rządu Składkowskiego",  Date='1936-05-16', Parent=["The Castle"]),
    dict(Resource="real",       Task="Wybory 1938",                     Date='1938-11-06', Parent=["Dissolve the Sejm"]), 
    dict(Resource="real",       Task="Nieprzyjęta dymisja rządu",       Date='1937-06-24', Parent=["Maintain the Dictatorship"]), 
]

previous_finish = dt.date(1936,1,1)
day = dt.timedelta(days=1)

def get_original(key, value, source):
    for shape in source:
        if shape[key] == value:
            return shape

for shape in source:
    if shape["Resource"] == "POL_focus":
        shape["Start"] = previous_finish
        shape["Finish"] = (shape["Start"] + shape["Duration"] * day)
        previous_finish = shape["Finish"]
        
        fig.add_shape(type="rect",
                      xref="x",
                      yref="y",
                      x0=shape["Start"].isoformat(),
                      y0=2,
                      x1=shape["Finish"].isoformat(),
                      y1=3,
                      line=dict(
                          color=focus_colors["politics"][0],
                          width=3,
                          ),
                      fillcolor=focus_colors["politics"][1],
                      )

for shape in source:
    if shape["Resource"] == "real":
        for parent in shape["Parent"]:
            original_task = get_original("Task", parent, source)
            
            start_point = original_task["Finish"].isoformat()
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
