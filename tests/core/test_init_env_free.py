import bulkhours


def test_init_env():
    kwargs = dict(email="yoda@jedi.com", database="data/cache/free1.json")
    print("test_init_env", kwargs)
    bulkhours.init_env(**kwargs)


def test_init_env2():
    kwargs = dict(email="luke.skywalker@jedi.com", database="data/cache/free1.json")
    print("test_init_env", kwargs)
    bulkhours.init_env(**kwargs)
