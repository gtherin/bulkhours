import bulkhours


data = """%%evaluation_cell_id -i synthetic

def generate_data(n=40):
    np.random.seed(1)
    df = pd.DataFrame(index=pd.date_range(start="2022", periods=n))
    df["is_test"] = df.index >= df.index[-15]
    # 1. Create a noise with an expected drift of 3 and a expected std of 0.3
    df["noise"] = sp.stats.norm(loc=3, scale=0.3).rvs(n) # BKRESET.INIT:0
    # 2. Create a trend with an expected increment of 1.7 and a expected std of 0.9
    df["trend"] = sp.stats.norm(loc=1.7, scale=0.9).rvs(n).cumsum() # BKRESET.INIT:0

    # 3. Add a seasonal signal
    df["seasonal"] = [0, 12, 0, 0]*int(n/4)

    # 4. Add a column with the sum of the trend and seasonal
    df["trend+seasonal"] = df["trend"] + df["seasonal"] # BKRESET.INIT:0
    return df

# Generate data
df = generate_data(n=40)

fig, axes = plt.subplots(ncols=4, figsize=(15, 4))
for i, variable in enumerate(["noise", "trend", "seasonal", "trend+seasonal"]):
    display(variable)
    ax = axes[i]
    # 4. Create analyses for the SimpleExp, Holt and 2xHolt-Winter models (one with a damp parameter of 0.96)
    # For each model, you should be able to compare the parameters.
    # BKRESET.REMOVE:START
    plot_prediction(df, {
        "Pred(1xExp)": exp_optimizer(df, variable),
        "Pred(2xExp)": exp_optimizer(df, variable, trend="add"),
        "Pred(3xExp)": exp_optimizer(df, variable, trend="add", seasonal="add", seasonal_periods=4),
        "Pred(3xExp, damped)": exp_optimizer(df, variable, trend="add", seasonal="add", seasonal_periods=4, damping_trend=0.96)
            }, variable, "Holt-Winters model", ax=ax)
    # BKRESET.REMOVE:END

# 5. Comment
print("... COMMENT...")  # BKRESET.REPLACE:print("... COMMENT...")
"""

def test_cell_reset():
    code = bulkhours.admin.cell_reset(data.split("\n"))



def test_cell_solution():
    code = bulkhours.admin.cell_solution(data.split("\n"))
    if "BKRESET." in code:
        raise Exception("Should not be here")
