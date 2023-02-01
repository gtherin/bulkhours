import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.linear_model
import os
import random

random.seed(10)

#Get predictions from a matrix of observations and a given weight matrix
def getPred(x,W):
    return(np.matmul(x,W))


#Compute square loss
def Loss(y,ypred):
    l=(y-ypred)**2
    return(l.sum())


#Compute mean Square Error
def MSE(X,Y,W):
    return((1/X.shape[0])*sum((Y-np.matmul(X,W))**2))


def GradDesc(X,Y,learnRate=0.01,epochs=2000,reg=0):
    
    global cacheLoss
    cacheLoss=[None]*epochs
    
    Weights=np.random.rand(X.shape[1])
    
    Weights=np.array(Weights)
    Weights=Weights.reshape(-1,1)
    m=X.shape[0]
    
    for i in range(epochs):
        
        predictions=getPred(X,Weights)
        cacheLoss[i]=Loss(Y,predictions)
        
        Weights[0]=Weights[0]-(1/m)*learnRate*(np.matmul(X[:,0].transpose(),predictions-Y))
        
        for j in range(1,len(Weights)):
            
            Weights[j]=Weights[j]-(1/m)*learnRate*(np.matmul(X[:,j].transpose(),predictions-Y)+sum(np.dot(Weights[j],reg)))

    return(Weights)


cancerData=pd.read_csv('prostate.txt',delimiter='\t')

trainCancer=cancerData[cancerData.loc[:,'train']=='T']

testCancer=cancerData[cancerData.loc[:,'train']=='F']

x_train=trainCancer.drop(columns=['id','lpsa','train'])
y_train=trainCancer.loc[:,'lpsa']

x_test= testCancer.drop(columns=['id','lpsa','train'])
y_test=testCancer.loc[:,'lpsa']


x_train_scaled=sklearn.preprocessing.scale(x_train, axis=0, with_mean=True, with_std=True, copy=True)

x_test_scaled=sklearn.preprocessing.scale(x_test, axis=0, with_mean=True, with_std=True, copy=True)

# Turn into numpy arrays with appropriate shape


x_train_scaled=np.array(x_train_scaled)
y_train=np.array(y_train)
y_train=y_train.reshape(-1,1)

y_test=np.array(y_test)
y_test=y_test.reshape(-1,1)

# Add a column of ones to represent the bias terms


addBias=np.ones([x_train_scaled.shape[0],1])

x_train_scaled=np.append(addBias,x_train_scaled,axis=1)

addBias=np.ones([x_test_scaled.shape[0],1])
x_test_scaled=np.append(addBias,x_test_scaled,axis=1)



# LEAST SQUARES

Wlinear=GradDesc(x_train_scaled,y_train)


LinearMSE=MSE(x_test_scaled,y_test,Wlinear)


# Form validation data for training hyperparameters

X_train, X_Validate, Y_train, Y_Validate = sklearn.model_selection.train_test_split( x_train_scaled, y_train, test_size=0.33, random_state=42)


def getRidgeLambda(x,y):
    
    bestMSE=10e100
    
    lamList=[l*0.05 for l in range(0,300)]

    global ridgeLambda
    
    for l in lamList:
        Wr=GradDesc(x,y,reg=l)
        if MSE(X_Validate,Y_Validate,Wr)< bestMSE:
            bestMSE=MSE(X_Validate,Y_Validate,Wr)
            ridgeLambda=l
          
    
    return(ridgeLambda)


ridgeLambda=getRidgeLambda(X_train, Y_train)

print(f'The ideal lambda for ridge, according to CV is {ridgeLambda}')

Wridge=GradDesc(x_train_scaled,y_train,reg=ridgeLambda)
RidgeMSE=MSE(x_test_scaled,y_test,Wridge)


def getLassoLambda(x,y):
    bestMSE=10e100
    
    alphaList=[l*0.1 for l in range(1,200)]
    
    
    for a in alphaList:
        lassoModel=sklearn.linear_model.Lasso(alpha=a,max_iter=5000,fit_intercept=False)
        lassoModel.fit(x,y)
        getPred=lassoModel.predict(X_Validate).reshape(-1,1)
        
        MSE=sum((Y_Validate-getPred)**2)
        if MSE < bestMSE:
            bestMSE=MSE
            lassoLambda=a

            
    return(lassoLambda)

lassoLambda=getLassoLambda(X_train,Y_train)

print(f'The ideal lambda for Lasso is {lassoLambda}')


fitLasso=sklearn.linear_model.Lasso(alpha=lassoLambda,fit_intercept=False)
fitLasso.fit(x_train_scaled,y_train)
Wlasso=fitLasso.coef_
pz=fitLasso.predict(x_test_scaled).reshape(-1,1)
LassoMSE=(1/x_test_scaled.shape[0])*sum((y_test-pz)**2)

def getParametersElasticNet(x,y):
    bestMSE=10e100
    
    regList=[l*0.1 for l in range(1,500)]
    ratio=[i*0.1 for i in range(1,200)]

    global bestAlpha
    global bestRatio
    global bestElasticWeights
    
    for l1 in regList:
        for r in ratio:
            elasticModel=sklearn.linear_model.ElasticNet(alpha=l1,l1_ratio=r,fit_intercept=False,max_iter=3000,tol=1e-5)
            elasticModel.fit(x,y)
            getPred=elasticModel.predict(X_Validate).reshape(-1,1)
        
            MSE=sum((Y_Validate-getPred)**2)
            if MSE< bestMSE:
                bestMSE=MSE
                bestAlpha=l1
                bestRatio=r
                bestElasticWeights=elasticModel.coef_
                
    return(bestElasticWeights)

elasticWeights=getParametersElasticNet(X_train,Y_train)


print(f'The ideal alpha for elastic net is {bestAlpha} and the best ratio is {bestRatio}')


fitElastic=sklearn.linear_model.ElasticNet(alpha=bestAlpha,l1_ratio=bestRatio,fit_intercept=False)
fitElastic.fit(x_train_scaled,y_train)
Welastic=fitElastic.coef_
pz=fitElastic.predict(x_test_scaled).reshape(-1,1)
ElasticMSE=(1/x_test_scaled.shape[0])*sum((y_test-pz)**2)
print(ElasticMSE)