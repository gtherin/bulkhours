import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.linear_model
import os
import random
from ..core import data

random.seed(10)


def MSE(X, Y, W):
    return (1 / X.shape[0]) * sum((Y - np.matmul(X, W)) ** 2)


def gradient_descent(X, Y, learnRate=0.01, epochs=2000, reg=0):

    weights = np.random.rand(X.shape[1]).reshape(-1, 1)
    alpha = learnRate / X.shape[0]

    for i in range(epochs):
        ydiff = np.matmul(X, weights) - Y

        for j in range(len(weights)):
            weights[j] -= alpha * np.matmul(X[:, j].transpose(), ydiff)
        for j in range(1, len(weights)):
            weights[j] -= alpha * sum(np.dot(weights[j], reg))

    return weights


def main1():
    cancerdf = data.get_data("prostate.tsv").reset_index()

    trainCancer, testCancer = cancerdf[cancerdf.loc[:, "train"] == "T"], cancerdf[cancerdf.loc[:, "train"] == "F"]
    x_train, y_train = trainCancer.drop(columns=["id", "lpsa", "train"]), trainCancer.loc[:, "lpsa"]
    x_test, y_test = testCancer.drop(columns=["id", "lpsa", "train"]), testCancer.loc[:, "lpsa"]

    # Turn into numpy arrays with appropriate shape
    x_train_scaled = sklearn.preprocessing.scale(x_train, axis=0, with_mean=True, with_std=True, copy=True)
    x_train_scaled = np.array(x_train_scaled)
    y_train = np.array(y_train).reshape(-1, 1)

    y_test = np.array(y_test).reshape(-1, 1)

    # Add a column of ones to represent the bias terms
    addBias = np.ones([x_train_scaled.shape[0], 1])
    x_train_scaled = np.append(addBias, x_train_scaled, axis=1)

    x_test_scaled = sklearn.preprocessing.scale(x_test, axis=0, with_mean=True, with_std=True, copy=True)
    addBias = np.ones([x_test_scaled.shape[0], 1])
    x_test_scaled = np.append(addBias, x_test_scaled, axis=1)

    # LEAST SQUARES
    Wlinear = gradient_descent(x_train_scaled, y_train)
    LinearMSE = MSE(x_test_scaled, y_test, Wlinear)

    # Form validation data for training hyperparameters
    X_train, X_Validate, Y_train, Y_Validate = sklearn.model_selection.train_test_split(
        x_train_scaled, y_train, test_size=0.33, random_state=42
    )


def getRidgeLambda(x, y, X_Validate, Y_Validate):
    bestMSE = 10e100

    lamList = [l * 0.05 for l in range(0, 300)]

    global ridgeLambda

    for l in lamList:
        Wr = gradient_descent(x, y, reg=l)
        if MSE(X_Validate, Y_Validate, Wr) < bestMSE:
            bestMSE, ridgeLambda = MSE(X_Validate, Y_Validate, Wr), l

    return ridgeLambda


def main2():
    ridgeLambda = getRidgeLambda(X_train, Y_train)

    print(f"The ideal lambda for ridge, according to CV is {ridgeLambda}")

    Wridge = gradient_descent(x_train_scaled, y_train, reg=ridgeLambda)
    RidgeMSE = MSE(x_test_scaled, y_test, Wridge)


def getLassoLambda(x, y):
    bestMSE = 10e100

    alphaList = [l * 0.1 for l in range(1, 200)]

    for a in alphaList:
        lassoModel = sklearn.linear_model.Lasso(alpha=a, max_iter=5000, fit_intercept=False)
        lassoModel.fit(x, y)
        getPred = lassoModel.predict(X_Validate).reshape(-1, 1)

        MSE = sum((Y_Validate - getPred) ** 2)
        if MSE < bestMSE:
            bestMSE = MSE
            lassoLambda = a

    return lassoLambda


def main3():
    lassoLambda = getLassoLambda(X_train, Y_train)

    print(f"The ideal lambda for Lasso is {lassoLambda}")

    fitLasso = sklearn.linear_model.Lasso(alpha=lassoLambda, fit_intercept=False)
    fitLasso.fit(x_train_scaled, y_train)
    Wlasso = fitLasso.coef_
    pz = fitLasso.predict(x_test_scaled).reshape(-1, 1)
    LassoMSE = (1 / x_test_scaled.shape[0]) * sum((y_test - pz) ** 2)


def getParametersElasticNet(x, y):
    bestMSE = 10e100

    regList = [l * 0.1 for l in range(1, 500)]
    ratio = [i * 0.1 for i in range(1, 200)]

    global bestAlpha
    global bestRatio
    global bestElasticWeights

    for l1 in regList:
        for r in ratio:
            elasticModel = sklearn.linear_model.ElasticNet(
                alpha=l1, l1_ratio=r, fit_intercept=False, max_iter=3000, tol=1e-5
            )
            elasticModel.fit(x, y)
            getPred = elasticModel.predict(X_Validate).reshape(-1, 1)

            MSE = sum((Y_Validate - getPred) ** 2)
            if MSE < bestMSE:
                bestMSE, bestAlpha, bestRatio, bestElasticWeights = MSE, l1, r, elasticModel.coef_

    return bestElasticWeights


def main4():
    elasticWeights = getParametersElasticNet(X_train, Y_train)

    print(f"The ideal alpha for elastic net is {bestAlpha} and the best ratio is {bestRatio}")

    fitElastic = sklearn.linear_model.ElasticNet(alpha=bestAlpha, l1_ratio=bestRatio, fit_intercept=False)
    fitElastic.fit(x_train_scaled, y_train)
    Welastic = fitElastic.coef_
    pz = fitElastic.predict(x_test_scaled).reshape(-1, 1)
    ElasticMSE = (1 / x_test_scaled.shape[0]) * sum((y_test - pz) ** 2)
    print(ElasticMSE)
