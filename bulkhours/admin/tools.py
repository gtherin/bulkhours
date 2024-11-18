import os
import subprocess
import datetime
import pandas as pd
import numpy as np
from .. import core


def switch_classroom(virtual_room, verbose=True, **kwargs):
    cfg = core.tools.get_config(is_new_format=True, **kwargs)
    if virtual_room is not None and virtual_room != cfg.virtual_room:
        if verbose:
            print(
                f"\x1b[35m\x1b[1mSwitching from {cfg.virtual_room} to {virtual_room}\x1b[m"
            )

        cfg["virtual_room"] = virtual_room
        core.tools.update_config(cfg)

    if verbose:
        if (
            "is_locked" in cfg[cfg.notebook_id]
            and (cfg.virtual_room + ";") in cfg[cfg.notebook_id]["is_locked"]
        ):
            print(
                f"⚠️\x1b[31m\x1b[41m\x1b[37mStudents can not submit answers '{cfg.notebook_id}/{cfg['virtual_room']}'\x1b[m⚠️"
            )
        elif (
            "is_locked" in cfg[cfg.notebook_id]
            and (cfg.virtual_room + ";") not in cfg[cfg.notebook_id]["is_locked"]
        ):
            print(
                f"\x1b[32m\x1b[1mStudents can submit answers for '{cfg.notebook_id}/{cfg['virtual_room']}'\x1b[m"
            )

    return cfg


def get_users_list(no_admin=True, sort_by=None, euser=None, cfg=None):
    if cfg is None:
        cfg = core.tools.get_config(is_new_format=True)
    virtual_room = cfg["virtual_room"]

    users = []
    if not no_admin:
        users += [
            (k, 1)
            for k in cfg.g["admins"]
            .replace(",", ";")
            .replace(" ", "")
            .replace(" ", "")
            .split(";")
            if k != ""
        ]
    users += [
        (k, 0)
        for k in cfg.g[virtual_room]
        .replace(",", ";")
        .replace(" ", "")
        .replace(" ", "")
        .split(";")
        if k != ""
    ]

    users = pd.DataFrame(users, columns=["mail", "is_admin"]).drop_duplicates(
        subset=["mail"]
    )

    # Add extra_user if not found
    if euser is not None and "@" in euser and euser not in users["mail"].unique():
        users = pd.concat(
            [
                users,
                pd.DataFrame.from_records(
                    [
                        {
                            "mail": euser,
                            "is_admin": 0,
                        }
                    ]
                ),
            ]
        )


    users["auser"] = users["mail"].str.split("@", n=1, expand=True)[0].str.capitalize()
    users["prenom"] = users["auser"]
    users["nom"] = ""

    for c in ["prenom", "nom", "mail", "auser"]:
        users[c] = users[c].astype(str)

    users = users[["auser", "prenom", "nom", "mail", "is_admin"]]
    if sort_by is not None:
        users = users.sort_by(sort_by)

    users.index = range(len(users))

    return users


def update_github(update_git, files=".", msg="Add cache files", verbose=True):
    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config = core.tools.get_config()

    if update_git and verbose:
        cmd = (
            f" à {uptime} pour '{config['subject']}/{config['virtual_room']}'. Mise à jour sur le cloud"
            if config["global"]["language"] == "fr"
            else f" at {uptime} for '{config['subject']}/{config['virtual_room']}'. Update on the cloud"
        )

        print(f"\x1b[32m\x1b[1m{msg}{cmd}\x1b[m")
    directory = os.path.dirname(__file__) + "/.."

    with open("git_push.sh", "w") as f:
        f.write(
            f"""cd {directory}
# Configure git config info to avoid errors
git config --global user.email "contact@bulkhours.fr" && git config --global user.name "bulkhours.fr" 2> /dev/null
git pull 2> /dev/null
"""
        )
        if type(files) == str:
            f.write(f"git add {files} 2> /dev/null\n")
        else:
            for gf in files:
                f.write(f"git add {gf} 2> /dev/null\n")
        f.write(f"""git commit -m "{msg}" 2> /dev/null\n""")
        f.write("git push 2> /dev/null")

    if update_git:
        print(
            subprocess.run(
                "bash git_push.sh".split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            ).stdout
        )
        os.system("rm -rf git_push.sh")
    elif verbose:
        cmd = (
            f" à {uptime} pour {config['subject']}/{config['virtual_room']}. Mise à jour locale"
            if config["global"]["language"] == "fr"
            else f" at {uptime} for {config['subject']}/{config['virtual_room']}. Update locally"
        )

        print(f"\x1b[32m\x1b[1m{msg}{cmd}\x1b[m")


def sort_by(sdata, icolumns=["auser"], sorted_by=True):
    if sorted_by:
        if type(sorted_by) in [str, list]:
            sdata = sdata.sort_values(sorted_by)
        else:
            sdata = sdata.sort_values(icolumns)
    return sdata


def styles(sdata, cmap="RdBu", icolumns=["auser"], sorted_by=True, hide_grades=False):

    if "nom" in sdata:
        sdata = sdata.drop(columns=["nom"])

    core.Grade.set_static_style_info(minvalue=0.0, cmap=cmap)

    if hide_grades:
        sdata = sdata.drop(columns=["all"])

    fcolumns = [c.replace(".n", "") for c in sdata.columns if c not in icolumns]
    nacolumns = [c for c in fcolumns if "all" not in c and c not in ["virtual_room"]]
    sdata = sdata.sort_index()
    sdata = sdata.rename(columns={c + ".n": c for c in fcolumns})

    for c in nacolumns:
        if c in sdata.columns:
            sdata[c] = sdata[c].replace(core.Grade.ANSWER_FOUND, np.nan)
            if hide_grades:
                sdata[c] = sdata[c].where(sdata[c] < 0, other=np.nan)

    stylish = sdata.style.hide(axis="index").format(precision=1, subset=list(fcolumns))
    stylish = stylish.background_gradient(cmap=cmap, vmin=0, vmax=10)

    ccols = [
        c
        for c in list(fcolumns)
        if c not in ["all", "virtual_room"]
        and core.tools.REF_USER in sdata[c]
        and sdata[c][core.tools.REF_USER] > 0
    ]

    def interpret_corr(v):
        return core.Grade.apply_style(v, True)

    stylish = stylish.map(interpret_corr, subset=ccols)

    nccols = [c for c in list(fcolumns) if c not in ccols]

    def interpret_ncorr(v):
        return core.Grade.apply_style(v, False)

    stylish = stylish.map(interpret_ncorr, subset=nccols)

    if "virtual_room" in sdata.columns:
        vrooms = sdata["virtual_room"].unique()
        cc = core.colors.color_maps(None)
        colors = {
            v: f"opacity: 60%;font-weight: bold;color: white;background-color: {cc[i]};"
            for i, v in enumerate(vrooms)
        }
        stylish = stylish.map(lambda v: colors[v], subset=["virtual_room"])

    if "all" in sdata.columns:
        stylish = stylish.background_gradient(
            cmap=cmap, subset=["all"], vmin=0, vmax=20.0
        )
        stylish = stylish.map(core.Grade.apply_all_style, subset=["all"])

    return stylish.set_properties().format("{:.1f}", na_rep="✅", subset=nacolumns)


def call_webhooks(whid):
    import os
    import requests

    url = whid.format(BULK_DBS=os.environ["BULK_DBS"], IPADDRESS=os.environ["IPADDRESS"])
    response = requests.get(url)

    # Check the status code
    if response.status_code == 200:
      # Request was successful
      data = response.json()  # If the response is JSON
      # Process the data
      print(data)  
    else:
      # Request failed
      print(f"Request failed with status code: {response.status_code}")