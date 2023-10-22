import bulkhours


def check_info(cmd, func_id="bulkhours.is_equal"):
    info = bulkhours.core.LineParser.get_func_args(cmd, func_id=func_id)
    print(cmd)
    print(info)
    return info


def test_get_equals_student_evaluation_function():
    info = check_info(cmd:="""def student_evaluation_function():""", func_id="student_evaluation_function")
    info = check_info(cmd:="""def student_evaluation_function(debug=True, run=True):""", func_id="student_evaluation_function")

def test_cell_parser():
    cell_content = """%%evaluation_cell_id -i synthetic

def generate_data(n=40):
    np.random.seed(1)

    # 1. Create a noise with an expected drift of 3 and a expected std of 0.3
    df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BKRESET.INIT:0

    # 2. Create a trend with an expected increment of 1.7 and a expected std of 0.9
    df["trend"] = sp.stats.norm(loc=1.7, scale=0.9).rvs(n).cumsum() # BKRESET.INIT:0

    # 4. Add a column with the sum of the trend and seasonal
    df["trend+seasonal"] = df["trend"] + df["seasonal"] # BKRESET.INIT:0
    return df

df = generate_data(n=40)

fig, axes = plt.subplots(ncols=4, figsize=(15, 4))
for i, variable in enumerate(["noise", "trend", "seasonal", "trend+seasonal"]):
    ax = axes[i]
    # 4. Create analyses for the SimpleExp, Holt and 2xHolt-Winter models (one with a damp parameter of 0.96)
    # BKRESET.REMOVE:START
    a = 3
    a = 4
    # BKRESET.REMOVE:END

def student_evaluation_function():
    a = 3
    return bulkhours.is_equal(student.flops, max_score=3)

# 5. Comment
print("... COMMENT...")  # BKRESET.REPLACE:print("... COMMENT...")
"""

    cinfo = bulkhours.core.LineParser.from_cell_id_user("synthetic", "solution")
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(cinfo=cinfo, data=cell_content, user="solution")
    print(teacher_data.minfo.keys())
    print(teacher_data.get_solution())
    print(teacher_data.get_reset())


def test_get_func_args():

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
    info = check_info(cmd:="""return bulkhours.is_equal(data_test, 3, max_score=5, policy="gaussian", error=1e-8)""")

