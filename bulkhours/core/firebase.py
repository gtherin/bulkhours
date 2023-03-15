import datetime
import os

from .logins import *


def get_document(sid, user):
    if "STUDENT" not in os.environ:
        set_up_student(None)

    from google.cloud import firestore

    return firestore.Client().collection(sid).document(user)


def send_answer_to_corrector(question, update=True, user=None, comment="", update_time=True, **kwargs):
    user = os.environ["STUDENT"] if user is None else user

    if update_time:
        kwargs.update({"update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    if update and get_document(question, user).get().to_dict():
        get_document(question, user).update(kwargs)
    else:
        get_document(question, user).set(kwargs)
    print(f"Answer {comment} has been submited for: {question}/{user}. You can resubmit it several times")


def get_solution_from_corrector(question, corrector="solution"):
    return get_document(question, corrector).get().to_dict()
