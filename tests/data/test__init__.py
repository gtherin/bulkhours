import bulkhours


# Test the get_data functions
def test_train():
    bulkhours.get_data("train_catvnoncat.h5")
    print(bulkhours.get_data("train_catvnoncat.h5", key="train_set_x"))

    return

    train_set_x_orig = bulkhours.get_data(
        "train_catvnoncat", key="train_set_x", credit=False
    )  # your train set features
    train_set_y_orig = bulkhours.get_data("train_catvnoncat", key="train_set_y", credit=False)  # your train set labels
    test_set_x_orig = bulkhours.get_data("test_catvnoncat", key="test_set_x", credit=False)  # your test set features
    test_set_y_orig = bulkhours.get_data("test_catvnoncat", key="test_set_y", credit=False)  # your test set labels
    classes = bulkhours.get_data("test_catvnoncat", key="list_classes", credit=False)  # the list of classes
