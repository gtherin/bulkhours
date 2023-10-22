import bulkhours


cell_content = """%%evaluation_cell_id -i synthetic

def generate_data(n=40):
    np.random.seed(1)
    df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BKRESET.INIT:0
    df["trend"] = sp.stats.norm(loc=1.7, scale=0.9).rvs(n).cumsum() # BKRESET.INIT:0
    df["trend+seasonal"] = df["trend"] + df["seasonal"] # BKRESET.INIT:0
    return df

fig, axes = plt.subplots(ncols=4, figsize=(15, 4))
for i, variable in enumerate(["noise", "trend", "seasonal", "trend+seasonal"]):
    ax = axes[i]
    # BKRESET.REMOVE:START
    a = 3
    a = 4
    # BKRESET.REMOVE:END

def student_evaluation_function():
    a = 3
    return bulkhours.is_equal(student.flops, max_score=3)

# 5. Comment
print("BK ROCKS")  # BKRESET.REPLACE:print("...COMMENT...")
"""

def test_cell_reset():
    cinfo = bulkhours.core.LineParser.from_cell_id("synthetic")
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(cinfo=cinfo, user="solution", data=cell_content)
    code = teacher_data.get_reset()
    print(code)

    if "BK ROCKS" in code:
        raise Exception("Should not be here")

    if "student_evaluation_function" in code:
        raise Exception("Should not be here")

def test_cell_solution():
    cinfo = bulkhours.core.LineParser.from_cell_id("synthetic")
    teacher_data = bulkhours.core.cell_parser.CellParser.crunch_data(cinfo=cinfo, user="solution", data=cell_content)
    code = teacher_data.get_solution()
    print(code)

    if "BKRESET." in code:
        raise Exception("Should not be here")

    if "...COMMENT..." in code:
        raise Exception("Should not be here")

    if "student_evaluation_function" in code:
        raise Exception("Should not be here")
