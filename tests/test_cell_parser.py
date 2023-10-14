import bulkhours


def check_info(cmd):
    info = bulkhours.core.cell_parser.get_equals_args(cmd)
    print(cmd)
    print(info)
    return info

def test_get_equals_args():

    info = check_info(cmd:="""return bulkhours.is_equal(np.array([1, 2, 3]))""")
    if info["data_ref"] != info["data_test"].replace("student.", "teacher."):
        raise(f"Error {cmd}\n{info}\n")

    info = check_info(cmd:="""return bulkhours.is_equal(data_test=np.array([1, 2, 3]))""")
    if info["data_ref"] != info["data_test"].replace("student.", "teacher."):
        raise(f"Error {cmd}\n{info}\n")

    info = check_info(cmd:="""score += bulkhours.is_equal(student.forward_one(A_prev, W, b, activation = "sigmoid")[0], max_score=1)""")
    if info["data_ref"] != info["data_test"].replace("student.", "teacher."):
        raise(f"Error {cmd}\n{info}\n")

    info = check_info(cmd:="""score += bulkhours.is_equal(student.forward_all(X, parameters)[0], max_score=3)""")

    info = check_info(cmd:="""score += bulkhours.is_equal(student.backward_one(dAL, linear_activation_cache, activation = "sigmoid"), max_score=3) #Checking the exact value.""")

    info = check_info(cmd:="""return bulkhours.is_equal(my_func(data), teacher.my_func(data), error=1e-8)""")
    if info != {'data_test': 'my_func(data)', 'data_ref': 'teacher.my_func(data)', 'error': '1e-8'}:
        raise(f"Error {cmd}\n{info}\n")

    info = check_info(cmd:="""return bulkhours.is_equal(data_test, data_ref=0.9525741268)""")
    info = check_info(cmd:="""return bulkhours.is_equal(data_test, data_ref=np.array([1, 2, 3]), max_score=5, policy="strict", error=1e-8)""")
    info = check_info(cmd:="""return bulkhours.is_equal(data_test, data_ref=3, max_score=5, policy="gaussian", error=1e-8)""")

