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
fig.update_yaxes(range=[-1, 4.5])

focus_colors= {
    "politics": ("Gray", "Silver"),
    "economy": ("DarkOrange", "Orange"),
    "marine": ("RoyalBlue", "LightSkyBlue"),
    "military": ("DarkOliveGreen", "Olive")
}


source = [
    dict(Resource="POL_focus",  Task="Complete the April Constitution",        Duration=70,    Type="politics"),
    dict(Resource="POL_focus",  Task="The Four Year Plan",                     Duration=35,    Type="economy"),
    dict(Resource="POL_focus",  Task="Central Region Strategy",                Duration=35,    Type="economy"),
    dict(Resource="POL_focus",  Task="The New Polish Industry",                Duration=35,    Type="economy"),
    dict(Resource="POL_focus",  Task="Fill the Railway Gaps",                  Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="Polish Militarism",                      Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Consolidate the Sanation Government",    Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Agrarian Reform",                        Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="The Castle",                             Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Central Defence of Poland",              Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="The Sanation Right",                     Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Eliminate the Socialist Parties",        Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Develop Upper Silesia",                  Duration=35,    Type="economy"),
    dict(Resource="POL_focus",  Task="Polish School of Mathematics",           Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="Dissolve the Sejm",                      Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Support Right Wing Paramilitarism",      Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Department of Home Defence",             Duration=35,    Type="politics"),
    dict(Resource="POL_focus",  Task="Develop Polish Shipbuilding",            Duration=70,    Type="marine"),
    dict(Resource="POL_focus",  Task="Attract Poles to Gdynia",                Duration=70,    Type="marine"),
    dict(Resource="POL_focus",  Task="Study British Ship Designs",             Duration=70,    Type="marine"),
    dict(Resource="POL_focus",  Task="Expand the Gdynia Seaport",              Duration=70,    Type="marine"),
    dict(Resource="POL_focus",  Task="Second Man of the State",                Duration=70,    Type="politics"),
    dict(Resource="POL_focus",  Task="Invest in the Old Polish Region",        Duration=35,    Type="economy"),
    dict(Resource="POL_focus",  Task="Modernise the Congressional Factories",  Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="Warsaw Main Railway Station",            Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="Invest in Eastern Poland",               Duration=70,    Type="economy"),
    dict(Resource="POL_focus",  Task="National Defense Fund",                  Duration=70,    Type="economy"),
    dict(Resource="real",       Task="Powołanie rządu Składkowskiego",  Date='1936-05-16', Parent=["The Castle"]),
    dict(Resource="real",       Task="Wybory 1938",                     Date='1938-11-06', Parent=["Dissolve the Sejm"]), 
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
                      y1=4.5,
                      line=dict(
                          color=focus_colors[shape["Type"]][0],
                          width=3,
                          ),
                      fillcolor=focus_colors[shape["Type"]][1],
                      )
        fig.add_annotation(
            x=(shape["Start"] + (shape["Finish"]-shape["Start"])/2).isoformat(),
            y=2,
            text=shape["Task"],
            showarrow=False,
            arrowhead=1,
            yshift=0,
            textangle=-90,
            yanchor="bottom",
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
            
            fig.add_annotation(
            x=end_point,
            y=1,
            text=shape["Task"],
            showarrow=False,
            textangle=-90,
            yanchor="top",
            )

        
        
fig.show()
