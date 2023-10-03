from .. import core
from . import tools
from . import answers


def cache_answers(cell_ids, update_git=False, verbose=True, **kwargs):
    for cell_id in cell_ids:
        cache_answer(cell_id, update_git=False, verbose=verbose, **kwargs)

    config = core.tools.get_config()

    msg = (
        f"Mise en cache des réponses de '{','.join(cell_ids)}'"
        if config["global"]["language"] == "fr"
        else f"Cache answers of '{','.join(cell_ids)}'"
    )

    tools.update_github(update_git, msg=msg, verbose=verbose)


def cache_answer(cell_id, **kwargs):
    answers.get_answers(cell_id, **kwargs)
