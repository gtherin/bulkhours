import IPython
import difflib
import pandas as pd
from scipy.spatial.distance import squareform
import scipy.cluster.hierarchy as shr
import numpy as np
import matplotlib.pyplot as plt


from .. import core
from . import answers
from . import tools


def leadlags(cell_id, **kwargs):
    cell_answers = answers.get_answers(cell_id, **kwargs)
    cfg = core.tools.get_config(is_new_format=True)
    cinfo = core.LineParser.from_cell_id_user(cell_id, core.tools.REF_USER)
    teacher_data = core.CellParser.crunch_data(cinfo=cinfo, data=cell_answers[core.tools.REF_USER] if core.tools.REF_USER in cell_answers else "", user=core.tools.REF_USER)

    users = tools.get_users_list(no_admin=False)

    ranswers, tanswers = {}, {}

    ranswers["reset"] = teacher_data.get_reset()
    ranswers["solution"] = teacher_data.get_solution()
    
    ranswers["reset"] = teacher_data.get_reset()
    ranswers["solution"] = teacher_data.get_solution()
    
    for u in users.index:
        mail, auser = users["mail"][u], users["auser"][u]
        cinfo = core.LineParser.from_cell_id_user(cell_id, mail)
        student_data = core.CellParser.crunch_data(cinfo=cinfo, data=cell_answers[mail] if mail in cell_answers else "", user=mail)
        ranswers[auser] = student_data.get_solution()
        tanswers[auser] = student_data.get_update_time()

    data = []
    for k1, v1 in ranswers.items():
        data.append([])
        for k2, v2 in ranswers.items():
            data[-1].append(difflib.SequenceMatcher(None, v1, v2).ratio())

    dist = pd.DataFrame(data, index=ranswers.keys(), columns=ranswers.keys())

    # Hierarchcial clustering
    p_dist = squareform(dist, checks=False)
    clustering = shr.linkage(p_dist, method="ward", optimal_ordering=True)

    # Ordering clusterings
    permutation = shr.leaves_list(clustering)
    permutation = permutation.tolist()
    # optimal number of clusters

    k = 10
    orientation = "left"
    labels = np.array(dist.keys())
    clusters_labels=[]

    fig, ax = plt.subplots(figsize=(10, 10))

    _, nodes = shr.to_tree(clustering, rd=True)
    nodes = [i.dist for i in nodes]
    nodes.sort()
    nodes = nodes[::-1][: k - 1]
    color_threshold = np.min(nodes)

    clusters = shr.cut_tree(clustering, n_clusters=k)

    clustos = {}
    for u in range(k):
        clustos[f"pool_{u}"] = []
        for idx, _ in enumerate(clusters):
            if clusters[idx][0] == u:
                clustos[f"pool_{u}"].append(labels[idx])

    #colors = af.color_list(k)

    #shr.set_link_color_palette(colors)
    shr.dendrogram(
        clustering, color_threshold=color_threshold, above_threshold_color="grey", ax=ax, orientation=orientation
    )
    shr.set_link_color_palette(None)

    if orientation == "top":
        ax.set_xticklabels(labels[permutation], rotation=90, fontsize=12, ha="center")
    else:
        ax.set_yticklabels(labels[permutation], fontsize=12)  # , rotation=90, ha="center")

    i = 0
    for coll in ax.collections[:-1]:  # the last collection is the ungrouped level
        xmin, xmax = np.inf, -np.inf
        ymin, ymax = np.inf, -np.inf
        for p in coll.get_paths():
            (x0, y0), (x1, y1) = p.get_extents().get_points()
            xmin = min(xmin, x0)
            xmax = max(xmax, x1)
            ymin = min(ymin, y0)
            ymax = max(ymax, y1)
        if orientation == "left":
            ymin = ymin - 4
            ymax = ymax + 4
            xwidth = (xmax - xmin) * 1.05
            ywidth = ymax - ymin
        else:
            xmin = xmin - 4
            xwidth = xmax - xmin + 4
            ywidth = (ymax - ymin) * 1.05
        rec = plt.Rectangle(
            (xmin, ymin),
            xwidth,
            ywidth,
            #facecolor=colors[i],
            alpha=0.2,
            edgecolor="none",
        )
        ax.add_patch(rec)
        if orientation == "left" and len(clusters_labels) > i and clusters_labels[i] != "":
            ax.text(
                xmin + xwidth + 0.02,
                ymin + 0.5 * ywidth,
                clusters_labels[i],
                rotation=90,
                va="center",
                ha="center",
                color=colors[i],
            )
        i += 1

    if orientation == "left":
        return ax
    ax.set_yticks([])
    ax.set_yticklabels([])
    for i in {"right", "left", "top", "bottom"}:
        side = ax.spines[i]
        side.set_visible(False)

    fig = plt.gcf()
    fig.tight_layout()

    return ax

