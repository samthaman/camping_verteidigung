import json
import plotly
import plotly.express as px


def plot_geo(df):
    fig = px.scatter_geo(df,
                        lat = df['description.geo.latitude'],
                        lon = df['description.geo.longitude'],
                        opacity=0.5,
                        # color=df['description.langArea'],
                        color= df['description.canton'],
                        hover_name = df['description.name'],
                        hover_data = [df.index]
    )

    fig.update_layout(
        height=450,
        width=700,
        margin={"r":0,"t":30,"l":0,"b":0},
        geo=dict(
            center=dict(
                lat=46.8182,
                lon=8.2275
            ),
            scope='europe',
            projection_scale=22,
            resolution = 50
            )
    )

    fig.update_geos(showsubunits=True)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON