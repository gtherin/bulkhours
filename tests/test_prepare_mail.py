import bulkhours


# Test the get_data functions
def test_prepare_mail():
    files = ["TP1b_Logistic_Regression.ipynb"]
    for f in files:
        bulkhours.admin.mail.copy(
            "contact@bulkhours.fr",
            "tests/",
            f,
            "john.doe@bulkhours.fr",
            reset=True,
            debug=False,
        )
