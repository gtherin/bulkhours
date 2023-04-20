import datetime
import os

from .logins import *


def get_document(sid, user):
    if "STUDENT" not in os.environ:
        set_up_student(None)

    if not os.path.exists(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]):
        set_up_student(os.environ["STUDENT"])

    from google.cloud import firestore

    return firestore.Client().collection(sid).document(user)


def send_answer_to_corrector(cinfo, update=True, user=None, comment="", update_time=True, **kwargs):
    question = cinfo.id
    user = os.environ["STUDENT"] if user is None else user

    corr = get_solution_from_corrector(question, corrector="solution")
    if corr is not None:
        print(
            f"\x1b[31m\x1b[1m The answer can not be submitted. Solution for {question} has already been submitted.  \x1b[m"
        )
        return

    uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if update_time:
        kwargs.update({"update_time": uptime})
    if user == "solution":
        kwargs.update({"note": 10})

    if update and get_document(question, user).get().to_dict():
        get_document(question, user).update(kwargs)
    else:
        get_document(question, user).set(kwargs)
    print(
        f"\x1b[32m\x1b[1m Answer {comment} has been submited at {uptime} for {question}/{user}. You can resubmit it several times \x1b[m"
    )


def get_solution_from_corrector(question, corrector="solution"):
    return get_document(question, corrector).get().to_dict()
