import datetime

from .. import data


def plot_roadmap(
    user,
    info,
    name="global",
    colors=None,
    bg_color=None,
    marker=None,
    sdate=None,
    edate=None,
):
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd

    df = data.get_data(info[user]["roadmap"], credit=False)
    df = df.query("tline>=0")
    df = df.query(f"roadmap == '{name}'").copy()
    # df["start_date"] = df["start_date"].map()
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    if marker is None:
        marker = "red"

    if colors is None:
        colors = [
            "#52DE97",
            "#FF5733",
            "#C70039",
            "#0097B2",
            "#FBE555",
            "#581845",
            "black",
            "#C70039",
            "#FF5733",
            "#0097B2",
            "#52DE97",
            "#FBE555",
        ]

    if type(colors) == list:
        colors = {c: colors[i] for i, c in enumerate(df.category.unique())}

    df["fcolorc"] = df["category"].map(colors)
    df["description"] = df["description"].fillna(df["task"])
    df["dash"] = df["dash"].fillna("solid")
    df["tcolor"] = df["tcolor"].fillna("white")
    df["fcolor"] = df["fcolor"].fillna(df["fcolorc"])
    df["lcolor"] = df["lcolor"].fillna(df["fcolorc"])
    df["tsize"] = df["tsize"].fillna(16)

    today = datetime.datetime.now()
    if sdate is None:
        sdate = df["start_date"].min()
    elif type(sdate) == int:
        sdate = today + datetime.timedelta(days=sdate)

    if edate is None:
        edate = df["end_date"].max()
    if type(edate) == int:
        edate = today + datetime.timedelta(days=edate)

    cats = {}
    fig = go.Figure()
    for i, d in df.iterrows():
        xmin, xmax = d["start_date"], d["end_date"]
        if xmin < sdate:
            xmin = sdate
        if xmax < sdate:
            xmax = sdate
        if xmin > edate:
            xmin = edate
        if xmax > edate:
            xmax = edate

        kwargs = dict(
            y=[
                -d.tline - 0.45,
                -d.tline - 0.45,
                -d.tline + 0.45,
                -d.tline + 0.45,
                -d.tline - 0.45,
            ],
            mode="lines",
            name=d.category,
            meta=[d.description],
            hovertemplate="%{meta[0]}<extra></extra>",
            legendgroup=d.category,
            line=dict(color=d.lcolor, width=4, dash=d.dash),
            fill="toself",
            fillcolor=d.fcolor,
        )

        if xmin < today:
            fig.add_trace(
                go.Scatter(
                    x=[xmin, today, today, xmin, xmin],
                    opacity=0.6,
                    showlegend=False,
                    **kwargs,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[today, xmax, xmax, today, today],
                    showlegend=d.category not in cats,
                    **kwargs,
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=[xmin, xmax, xmax, xmin, xmin],
                    showlegend=d.category not in cats,
                    **kwargs,
                )
            )

        if d.category not in cats:
            cats[d.category] = True

        fig.add_trace(
            go.Scatter(
                x=[xmin + 0.5 * (xmax - xmin)],
                y=[-d.tline],
                mode="text",
                legendgroup=d.category,
                text=[d.task],
                hoverinfo="skip",
                textposition="middle center",
                textfont=dict(color=d.tcolor, size=d.tsize),
                showlegend=False,
            )
        )

    if bg_color is None:
        bg_color = "rgba(0,0,0,0)"

    fig.add_vline(x=today, line_width=4, line_color=marker)
    fig.update_layout(
        template="plotly_dark",
        title="",
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=False,
        width=1000,
        height=400,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(tickfont=dict(size=16)),
        legend=dict(orientation="h", font=dict(size=22), x=0.15, y=1.1),
    )

    fig.update_layout(xaxis=dict(range=[sdate, today + datetime.timedelta(days=100)]))

    fig.update_yaxes(visible=False)
    fig.update_xaxes(gridcolor="white")

    fig.show()
    return
