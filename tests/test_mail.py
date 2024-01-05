import bulkhours


def test_mails():
    bulkhours.admin.send_mails(
        notebook_file="TP1b_Logistic_Regression.ipynb",
        drive_rdir="tests",
        dnotebook_files="tests/notebooks.json",
        fake=False,
    )


# Test the get_data functions
def test_mail():
    bulkhours.admin.send_mail(
        to="contact@bulkhours.fr, no-reply@bulkhours.fr",
        message="""
    <p>Dear <b>'you'</b>:</p>
This is only a test
    <ul><li><a href="https://bulkhours.fr" style="font-size: 18px; margin: 4px 0;background-color: white; color: #4F77AA; padding: 5px 9px; text-align: center; text-decoration: none; display: inline-block;">Course of the day</a></li></ul><br/><br/>
The BulkHours team (tribute to Foremost Poets)<br/>
<a href="mailto:contact@bulkhours.fr">contact</a>
""",
        title="SMTP test",
    )
