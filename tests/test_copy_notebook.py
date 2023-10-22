import os
import bulkhours


def test_copy_notebook():

    bulkhours.admin.mail.copy("yo.da@jedi.com", "examples/", "2_Course_Edition.ipynb", "john.doe@bulkhours.eu", reset=True, debug=False)

    os.system("rm -rf examples/2_Course_Edition_3*.ipynb")
