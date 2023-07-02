{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "toc_visible": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "gpuClass": "standard"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "# Install the package\n",
        "\n",
        "First, you need to install the package from github and import it:"
      ],
      "metadata": {
        "id": "cxb4MUu_VnLD"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Install the bulkhours package\n",
        "!rm -rf bulkhours && git clone https://github.com/guydegnol/bulkhours.git\n",
        "\n",
        "# import the bulkhours package\n",
        "import bulkhours\n",
        "\n",
        "# Generate header links\n",
        "bulkhours.generate_header_links(\"examples/6_Predict_Covid_Cases.ipynb\")"
      ],
      "metadata": {
        "id": "rSpNjxbXy0TB",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 175
        },
        "outputId": "ab604d7b-4a45-427b-8125-c5504b9ef307"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Cloning into 'bulkhours'...\n",
            "remote: Enumerating objects: 5159, done.\u001b[K\n",
            "remote: Counting objects: 100% (758/758), done.\u001b[K\n",
            "remote: Compressing objects: 100% (368/368), done.\u001b[K\n",
            "remote: Total 5159 (delta 474), reused 642 (delta 361), pack-reused 4401\u001b[K\n",
            "Receiving objects: 100% (5159/5159), 40.86 MiB | 10.84 MiB/s, done.\n",
            "Resolving deltas: 100% (3311/3311), done.\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.Markdown object>"
            ],
            "text/markdown": "\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/guydegnol/bulkhours/blob/main/examples/1_Simple_Exercice_Automation.ipynb) [![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/guydegnol/bulkhours/blob/main/examples/1_Simple_Exercice_Automation.ipynb) [![GitHub](https://badgen.net/badge/icon/Open%20in%20Github?icon=github&label)](https://github.com/guydegnol/bulkhours/blob/main/examples/1_Simple_Exercice_Automation.ipynb) [![Visual Studio](https://badgen.net/badge/icon/Open%20in%20Visual%20Studio?icon=visualstudio&label)](https://vscode.dev/github/guydegnol/bulkhours/blob/main/examples/1_Simple_Exercice_Automation.ipynb) [![CC-0 license](https://img.shields.io/badge/License-CC--0-blue.svg)](https://creativecommons.org/licenses/by-nd/4.0)\n                            "
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Create my first exercice\n",
        "\n",
        "\n",
        "**Exercise**: Using `numpy.exp`, implement the $\\sigma(z) = \\frac{1}{1 + e^{-z}}$ to make predictions. The expected solution is in the following cell:\n"
      ],
      "metadata": {
        "id": "WAWZ3hSUC_ju"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "%%evaluation_cell_id -i covid\n",
        "# Get and fit the data\n",
        "covid = bulkhours.get_data(\"covid\", credit=True, query=\"iso_code in ('FRA')\", index=\"date\")['new_cases']\n",
        "covid.index = pd.DatetimeIndex(covid.index).to_period('D')\n",
        "covid = covid.rolling(7).mean()[covid > 0].iloc[-500:]\n",
        "model = smtsa.SARIMAX(covid, order=(3, 0, 0), seasonal_order=(1, 1, 0, 31)).fit()\n",
        "\n",
        "# Plot the data\n",
        "fig, ax = plt.subplots(figsize=(12, 4))\n",
        "pd.Series(covid.values, index=covid.index.to_timestamp()).plot(ax=ax, label='Actual', alpha=0.6, lw=5, legend=True)\n",
        "pd.Series(model.fittedvalues.values, index=covid.index.to_timestamp()).plot(ax=ax, label='Trained', ls=\"dashed\", lw=2, legend=True)\n",
        "model.forecast(steps=30).plot(ax=ax, label='Predicted', ls=\"dotted\", legend=True);\n",
        "\n",
        "# Conclude\n",
        "IPython.display.Markdown(\"<h3>La situation devrait être sous controle dans le mois prochain en France.</h3>\")"
      ],
      "metadata": {
        "id": "uAq52jp3IMDd"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}