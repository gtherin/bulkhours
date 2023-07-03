import os
import subprocess
import datetime
import pandas as pd
import matplotlib
from .. import core


def switch_classroom(virtual_room, verbose=True):
    info = core.tools.get_config(is_new_format=True)
    if virtual_room is not None and virtual_room != info.virtual_room:
        if verbose:
            print(f"\x1b[35m\x1b[1mSwitching from {info.virtual_room} to {virtual_room}\x1b[m")

        info["virtual_room"] = virtual_room
        core.tools.update_config(info)
    return info


def get_users_list(no_admin=True):
    info = core.tools.get_config(is_new_format=True)
    virtual_room = info["virtual_room"]

    users = [
        (k, 0) for k in info.g[virtual_room].replace(",", ";").split(";") if k != "" and k not in info.g["admins"]
    ]
    if not no_admin:
        users += [(k, 1) for k in info.g["admins"].replace(",", ";").split(";") if k != ""]

    users = pd.DataFrame(users, columns=["mail", "is_admin"])

    new = users["mail"].str.split("@", n=1, expand=True)[0].str.split(".", n=1, expand=True)
    users["prenom"] = new[0].str.capitalize()
    users["nom"] = new[1].str.capitalize()

    users = pd.concat(
        [users, pd.DataFrame.from_records([{"mail": "solution", "is_admin": 1, "prenom": "Sol", "nom": "Ution"}])]
    )
    return users[["prenom", "nom", "mail", "is_admin"]]


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
git config --global user.email "bulkhours@guydegnol.net" && git config --global user.name "guydegnol" 2> /dev/null
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
                "bash git_push.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
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


def styles(data, cmap="RdBu"):
    import numpy as np

    maxcolor = matplotlib.colors.rgb2hex(matplotlib.cm.get_cmap(cmap)(1.0))

    def interpret(v):
        if v != v or v == -1:
            return "color:#FF3B52;background-color:#FF3B52;opacity: 20%;"
        # if np.abs(v) < 0.1:
        #    return f"color:{maxcolor};background-color:{maxcolor};"
        if np.abs(v + 2) < 0.1:  # Failure of automatic corrections
            return f"color:red;background-color:red;"
        return None

    fcolumns = [c.replace(".n", "") for c in data.columns if c not in ["nom", "prenom"]]
    nacolumns = [c for c in fcolumns if "all" not in c]

    sdata = data.sort_values(["nom", "prenom"]).rename(columns={c + ".n": c for c in fcolumns})
    stylish = sdata.style.hide(axis="index").format(precision=1, subset=list(fcolumns))
    stylish = (
        stylish.hide(axis="index")
        .background_gradient(cmap=cmap, vmin=0, vmax=10)
        .applymap(interpret, subset=list(fcolumns))
    )

    if "all" in sdata.columns:
        stylish = stylish.background_gradient(cmap=cmap, subset=["all"], vmin=0, vmax=10.0)

    return stylish.set_properties(**{"opacity": "70%"}, subset=nacolumns)
