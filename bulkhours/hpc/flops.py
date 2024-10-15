import pandas as pd  # library for data analysis
import requests  # library to handle requests
from bs4 import BeautifulSoup  # library to parse HTML documents


def get_html_object(wpage, in_table, wsite="https://en.wikipedia.org/wiki/", verbose=False, sclass="wikitable"):
    url = wsite + wpage
    print(f"""From {url}, getting data table whith string "{in_table}" in it""")

    # Get the page in the form of html
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    my_tables = (
        soup.find_all("table", {"class": "wikitable"})
        if sclass == "wikitable"
        else soup.find_all("td", {"class": "sidebar-content plainlist"})
    )

    for table in my_tables:
        if verbose:
            print(f"# New table: \n {str(table)}")
        if in_table in str(table):
            return str(table)


def get_engraving_scale(verbose=False):
    table = get_html_object(
        wpage="Transistor_count",
        in_table="800 nm",
        verbose=verbose,
        sclass="sidebar-content",
    )

    lines = BeautifulSoup(str(table), "html.parser").find_all("li")
    data = []
    for line in lines:
        year = str(line)[-9:-5]
        scale = line.find("a").get_text()
        scale = float(scale[:-3]) * 1000 if "µm" in scale else float(scale[:-3])
        data.append({"year": int(year), "scale": int(scale)})

    return pd.DataFrame.from_records(data)


def get_table_from_wiki(wpage, in_table, columns=None, wsite="https://en.wikipedia.org/wiki/", verbose=False):
    url = wsite + wpage
    from io import StringIO

    print(f"""From {url}, getting data table whith string "{in_table}" in it""")
    # Get the page in the form of html
    response = requests.get(url)

    # Parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, "html.parser")

    my_tables = soup.find_all("table", {"class": "wikitable"})
    for table in my_tables:
        if verbose:
            print(f"# New table: \n {str(table)}")
        if in_table in str(table):
            table_io = StringIO(str(table))
            data = pd.DataFrame(pd.read_html(table_io)[0])
            if columns is not None:
                data.columns = columns
            return data


class FLOPS:
    def __init__(self):
        print("""Data are https://en.wikipedia.org/wiki/FLOPS""")
        # Get the page in the form of html
        response = requests.get("https://en.wikipedia.org/wiki/FLOPS")

        # Parse data from the html into a beautifulsoup object
        soup = BeautifulSoup(response.text, "html.parser")
        my_tables = soup.find_all("table", {"class": "wikitable"})
        for table in my_tables:
            if "wikitable floatright" in str(table):
                self.units = pd.DataFrame(pd.read_html(str(table))[0])
            else:
                # convert list to dataframe
                costs = pd.DataFrame(pd.read_html(str(table))[0])
                costs.columns = ["date", "un_costs", "costs", "platform", "comments"]
                self.costs = costs[["date", "costs"]]

    def get_flop_factor(self):
        return self.units

    def get_costs(self):
        return self.costs


def get_tf_model(model_name, weights="imagenet", summary=False):
    import tensorflow as tf

    available_models = list(dir(tf.keras.applications))
    model = model_name
    if type(model_name) != str:
        pass
    elif model_name in available_models:
        model = getattr(tf.keras.applications, model_name)(weights=weights)
    else:
        print(f"Available models:\n{available_models}")

    if summary:
        model.summary()

    return model


def get_tf_flops(model_name, batch_size=None, verbose=True, summary=False, weights="imagenet"):
    import tensorflow as tf
    from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2_as_graph

    model = get_tf_model(model_name, weights=weights, summary=summary)

    if batch_size is None:
        batch_size = 1

    real_model = tf.function(model).get_concrete_function(
        tf.TensorSpec([batch_size] + list(model.inputs[0].shape[1:]), model.inputs[0].dtype)
    )
    frozen_func, graph_def = convert_variables_to_constants_v2_as_graph(real_model)

    run_meta = tf.compat.v1.RunMetadata()
    opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
    flops = tf.compat.v1.profiler.profile(graph=frozen_func.graph, run_meta=run_meta, cmd="op", options=opts)

    if verbose:
        print(f"{model.name}: {flops.total_float_ops:,} FLOPs,  {flops.total_float_ops/2:,} MACs ({weights})")
    return flops.total_float_ops
