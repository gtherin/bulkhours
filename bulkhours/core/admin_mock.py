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


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def generic_func(func, *kargs, **kwargs):
    try:
        import bulkhours_admin

        return func(*kargs, **kwargs)

    except ImportError:
        from .tools import get_config

        config = get_config()
        mock_message(config["in_french"])


def summary(*kargs, **kwargs):
    func = import_from("bulkhours_admin", "summary")
    return generic_func(func, *kargs, **kwargs)


def get_audio(*kargs, **kwargs):
    func = import_from("bulkhours_admin.audio", "get_audio")
    return generic_func(func, *kargs, **kwargs)


def evaluate(*kargs, **kwargs):
    from .tools import md

    func = import_from("bulkhours_admin", "evaluate")
    return generic_func(func, *kargs, md=md, **kwargs)
