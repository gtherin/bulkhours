import os
import bulkhours


def test_copy_notebook():
    cfg = bulkhours.core.tools.get_config(is_new_format=True)
    bulkhours.admin.mail.copy(
        "yo.da@jedi.com",
        "examples",
        "2_Course_Edition.ipynb",
        "john.doe@bulkhours.eu",
        reset=True,
        cfg=cfg,
        debug=False,
    )

    os.system("rm -rf examples/2_Course_Edition_3*.ipynb")


def test_copy4students():
    cfg = bulkhours.core.tools.get_config(is_new_format=True)
    bulkhours.admin.copy4students(
        "yo.da@jedi.com", "examples", "2_Course_Edition.ipynb", cfg=cfg
    )
    os.system(f"rm -rf examples/{cfg.virtual_room}")


def test_evaluate_notebook():
    bulkhours.core.firebase.init_database({})

    bulkhours.admin.nevaluate("tests/TP5_Music_generation_TISA.ipynb", fake=True)
