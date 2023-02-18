import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def geo_plot_country(data, ax, country_name, facecolor="None", edgecolor="red"):
    from descartes import PolygonPatch

    nami = data[data.name == country_name]
    namigm = nami.__geo_interface__["features"]  # geopandas's geo_interface
    namig0 = {"type": namigm[0]["geometry"]["type"], "coordinates": namigm[0]["geometry"]["coordinates"]}
    ax.add_patch(PolygonPatch(namig0, fc=facecolor, edgecolor=edgecolor, alpha=0.85, zorder=2))


def geo_plot(
    data=None,
    timeopt=None,
    column=None,
    legend=True,
    cmap="OrRd",
    ax=None,
    show_columns=False,
    hightlight=[],
    **kwargs,
):
    if data is None or column is None:
        print(f"data={data} column={column}")
        return

    if show_columns:
        print(list(data.columns.sort_values()))

    kwargs["missing_kwds"] = {"color": "lightgrey", "edgecolor": "white", "hatch": "///", "label": "Missing values"}
    kwargs.update(dict(legend=legend, legend_kwds={"shrink": 0.3}))

    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 10))
    data.plot(
        ax=ax,
        column=column,
        edgecolor="gray",
        cmap=cmap,
        **kwargs,
    )
    ax.set_axis_off()

    hcmap = plt.cm.get_cmap("jet")
    ccmap = plt.cm.get_cmap(cmap)

    legend_elements = []
    for ic, country in enumerate(hightlight):
        fcountry = data.query(f"name=='{country}'")
        if not fcountry.empty:
            color = hcmap(ic / len(hightlight))
            value = fcountry[column].iloc[0]
            geo_plot_country(data, ax, country, edgecolor=color)
            legend_elements.append(
                Patch(facecolor=ccmap(value), edgecolor=color, label=f"{country[:13]}: {value:.2f}")
            )

    ax.legend(handles=legend_elements, loc=3)
    ax.set_title(f"World map: {column} (time={timeopt})")

    return ax
