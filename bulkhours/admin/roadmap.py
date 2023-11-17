import datetime

from .. import data


def plot_roadmap(user, info, name="global", colors=None, bg_color=None, marker=None):

    import plotly.graph_objects as go

    df = data.get_data(info[user]["roadmap"], credit=False)
    df = df.query("tline>=0")
    df = df.query(f"roadmap == '{name}'")

    if marker is None:
        marker = "red"

    if colors is None:
        colors = ["#52DE97", "#FF5733", '#C70039', "#0097B2", '#FBE555', "#581845", "black", "#C70039", "#FF5733", "#0097B2", "#52DE97", "#FBE555"]

    if type(colors) == list:
        colors = {c: colors[i] for i, c in enumerate(df.category.unique())}

    df["fcolor"] = df["category"].map(colors)

    cats = {}
    fig = go.Figure()
    today = datetime.datetime.now()
    for i, d in df.iterrows():
        xmin, xmax = datetime.datetime.strptime(d["start_date"], '%Y-%m-%d'), datetime.datetime.strptime(d["end_date"], '%Y-%m-%d')
        ekwargs = eval("dict(" + str(d.kwargs) + ")") if type(d.kwargs) != float else {}
        tsize = 16 if "tsize" not in ekwargs else ekwargs["tsize"]
        tcolor = 'white' if "tcolor" not in ekwargs else ekwargs["tcolor"]
        fcolor = d.fcolor if "fcolor" not in ekwargs else ekwargs["fcolor"]
        lcolor = fcolor if "lcolor" not in ekwargs else ekwargs["lcolor"]
        dash = 'solid' if "dash" not in ekwargs else ekwargs["dash"]
        description = d.task if "description" not in ekwargs else ekwargs["description"]

        kwargs = dict(y=[-d.tline - 0.45, -d.tline - 0.45, -d.tline + 0.45, -d.tline + 0.45, -d.tline - 0.45],
                    mode='lines', name=d.category, meta=[description], hovertemplate='%{meta[0]}<extra></extra>',
                    legendgroup=d.category, line=dict(color=lcolor, width=4, dash=dash), fill='toself', fillcolor=fcolor)

        if xmin < today:
            fig.add_trace(go.Scatter(x=[xmin, today, today, xmin, xmin], opacity=0.6, showlegend=False, **kwargs))
            fig.add_trace(go.Scatter(x=[today, xmax, xmax, today, today], showlegend=d.category not in cats, **kwargs))
        else:
            fig.add_trace(go.Scatter(x=[xmin, xmax, xmax, xmin, xmin], showlegend=d.category not in cats, **kwargs))

        if d.category not in cats:
            cats[d.category] = True

        fig.add_trace(go.Scatter(x=[xmin + 0.5*(xmax-xmin)], y=[-d.tline], mode='text', legendgroup=d.category, text=[d.task], hoverinfo='skip', 
                                textposition="middle center", textfont=dict(color=tcolor, size=tsize), showlegend=False))

    if bg_color is None:
        bg_color = "rgba(0,0,0,0)"

    fig.add_vline(x=today, line_width=4, line_color=marker)
    fig.update_layout(template="plotly_dark", title="", margin=dict(l=0, r=0, t=0, b=0), autosize=False, 
                    width=1000, height=400, paper_bgcolor=bg_color, plot_bgcolor=bg_color)

    fig.update_yaxes(visible=False)
    fig.update_xaxes(gridcolor='white')
    fig.show()
    return

