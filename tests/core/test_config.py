import bulkhours


def test_config():
    config = bulkhours.get_config(is_new_format=True)

    print(config)

    for k, v in config.items():
        print(k, v)

    print(config.subject)
    print(config.language)
    print(config.norm20)
