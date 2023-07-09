import bulkhours


def test_help():
    bulkhours.data.build_readme(load_data=True)
    bulkhours.data.help()
