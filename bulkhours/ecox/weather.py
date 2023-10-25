

def get_wheather_data(longitude, latitude, altitude=0, start=None, end=None):
    import folium
    import datetime
    import IPython
    from folium.plugins import MarkerCluster
    from branca.element import Figure
    from meteostat import Point, Daily

    if start is None:
        start = datetime.datetime(1970, 1, 1)

    if end is None:
        end = datetime.datetime.now()

    fig = Figure(width=900, height=300)
    trimap = folium.Map(location=(longitude, latitude), zoom_start=13)
    fig.add_child(trimap)

    marker_cluster = MarkerCluster().add_to(trimap)
    folium.Marker(
                location=[longitude, latitude],
                popup="Weather coordonates",
                icon=folium.Icon(color="lightblue", icon_color="orange", icon="sun", angle=0, prefix="fa"),
            ).add_to(marker_cluster)

    IPython.display.display(trimap)

    df = Daily(Point(longitude, latitude, altitude), start, end).fetch()
    df.index.freq = "D"
    return df
