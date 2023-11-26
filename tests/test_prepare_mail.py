import bulkhours


# Test the get_data functions
def test_prepare_mail():
    files = ["TP1b_Logistic_Regression.ipynb"]
    for f in files:
        bulkhours.admin.mail.copy(
            "contact@bulkhours.eu",
            "tests/",
            f,
            "john.doe@ipsa.fr",
            reset=True,
            debug=False,
        )
