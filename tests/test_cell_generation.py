import bulkhours


data = """%%evaluation_cell_id -i synthetic

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

def test_cell_reset():
    code = bulkhours.admin.cell_reset(data)



def test_cell_solution():
    code = bulkhours.admin.cell_solution(data)
    if "BKRESET." in code:
        raise Exception("Should not be here")
