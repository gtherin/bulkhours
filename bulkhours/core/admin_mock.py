def is_admin():
    try:
        import bulkhours_admin

        return True
    except ImportError:
        return False


def evaluate(*kargs, **kwargs):
    from .tools import get_config

    config = get_config()
    if not is_admin():
        mock_message(config["in_french"])
        return
    from bulkhours_admin import summary

    summary(*kargs, **kwargs)


def evaluate(*kargs, **kwargs):
    from .tools import get_config

    config = get_config()
    if not is_admin():
        mock_message(config["in_french"])
        return

    from bulkhours_admin import evaluate

    evaluate(*kargs, **kwargs)


def mock_message(in_french):
    import IPython

    tooltip = (
        """
Les fonctionnalités 'evaluation_cell_id' ne sont plus disponibles😕.
Vous pouvez supprimer son appel de la cellule (pour enlever ce button) ou
contacter bulkhours@guydegnol.net pour avoir un nouveau token pour reactiver le service🚀"""
        if in_french
        else """
The 'evaluation_cell_id' functionalities are no more available😕. 
You can remove its call line from the cell (to remove that button) or
contact bulkhours@guydegnol.net to have a new token to reactivate the service🚀"""
    )

    IPython.display.display(tooltip)
