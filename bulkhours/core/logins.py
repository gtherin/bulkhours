

import os
import json

def get_cred(k="pi.pyc", d=None, pass_code=None):
    os.system(f"rm -rf {d}{k}")
    with open(d + k, "w") as f:
        f.write(
            open(f"{d}/pi.so")
            .read()
            .replace("eagezehrzqHHZHZ", "999d262597343d1840c218c3da3ec9c6f803aaf6")
            .replace("egzezqh234ehzqh22", pass_code)
        )
    return d + k


def clean_student_name(student_name):
    import unicodedata

    student_name = unicodedata.normalize("NFKD", student_name.replace("-", "").replace(" ", "").lower())
    return student_name.encode("ASCII", "ignore").decode("utf-8")


def set_up_student(student_name, pass_code=None):
    directory = os.path.dirname(__file__) + "/../bunker/"

    if pass_code is None:
        jsonfile = os.path.dirname(__file__) + "/../../.safe"
        if os.path.exists(jsonfile):
            with open(jsonfile) as json_file:
                data = json.load(json_file)
                pass_code = data["pass_code"]
    if student_name == "noraise":
        return

    # TODO: Fix that thing in the future
    # Ok till I have less-restrictive rules on the server side
    if student_name is None or student_name in ["None", ""] or pass_code is None or pass_code == "PASS_COURSE":
        raise Exception.DefaultCredentialsError(
            f"""# Register yourself (Password "PASS" should be given in class). Example for "John Doe", type:
bulkhours.set_up_student("john.d", pass_code="PASS")
"""
        )

    os.environ["STUDENT"] = clean_student_name(student_name)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_cred(d=directory, pass_code=pass_code)
    return student_name
