import numpy as np
import math
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
import itertools



def getRFEst(n_est, max_feat):
	rf = RandomForestClassifier(n_estimators = n_est, max_features = max_feat)
	return rf

def getCV(estimator, data, labels):
	return np.mean(cross_val_score(estimator, data, labels, cv = 5))

def getBestRFParam(data, labels, n_estMin = 1, n_estMax = 3000, 
		max_featMin = 1, max_featMax = 2000):
	minCV = math.inf
	minParam = [1,1]
	for n_est in range(n_estMin,n_estMax):
		for max_feat in range(max_featMin,max_featMax):
			rf = getRFEst(n_est, max_feat)
			cv = getCV(rf, data, labels)
			if cv < minCV:
				minCV = cv
				minParam = [n_est, max_feat]
	return minParam

#Return SVM with c parameter.
def getSVMEst(c):
	return svm.LinearSVC(C = c)

#Find c between cmin and cmax that returns the min CV of an SVM model.
def getBestSVMParam(data, labels, cmin = 0, cmax = 10000):
	minCV = math.inf
	minParam = 0
	for c in range(cmin,cmax):
		svm = getSVMEst(c)
		cv = getCV(svm, data, labels)
		if cv < minCV:
			minCV = cv
			minParam = c
	return minParam

#returns Kcluster estimator fitted on data.
def Kcluster(data):
	kmeans = KMeans(n_clusters = 5)
	kmeans.fit(data)
	return kmeans

#returns numpy array of indices corresponding to most important features.
def getImportantFeatInd(estimator, numFeats):
	importanceVector = np.array(estimators.feature_importances_)
	return np.array(importanceVector.argsort()[-numFeats:][::-1])

def getAccTot(estimator, trainingData, trainingLabels):
	return estimator.score(trainingData, trainingLabels)

def getClassAcc(estimator, trainingData, trainingLabels):
	pred = estimator.predict(trainingData)
	cmat = confusion_matrix(trainingLabels, pred)
	return cmat

def clusterAcc(estimator, trainingData, trainingLabels):
	kmeansPred = estimator.predict(trainingData)
	permutations = [i for i in itertools.permutations([0,1,2,3,4])]
	maxAcc = 0
	for order in permutations:
		newLabels = [order[i-1] for i in trainingLabels]
		newAcc = accuracy_score(newLabels, kmeansPred)
		if maxAcc < newAcc:
			maxAcc = newAcc
	return maxAcc



trainingData = 
trainingLabels = 
testData = 
testLabels = 
featureArray = np.array()


rfParam = getBestRFParam(trainingData, trainingLabels)			#Get parameters of best RF model
rfEst = getRFEst(rfParam[0], rfParam[1])						#Create RF estimator
top_10_RF_Feat = featureArray[getImportantFeatInd(rfEst,10)]	#Get top 10 important features of RF model
rfTotAcc = getAccTot(rfEst, trainingData, trainingLabels)
rfClassAcc = getClassAcc(rfEst, trainingData, trainingLabels)


svmParam = getBestSVMParam(trainingData, trainingLabels, 0, 1000)
svmEst = getSVMEst(svmParam)
top_10_SVM_Feat = featureArray[getImportantFeatInd(svmEst,10)]
svmTotAcc = getAccTot(svmEst, trainingData, trainingLabels)
svmClassAcc = getClassAcc(svmEst, trainingData, trainingLabels)


kmeansEst = Kcluster(trainingData[getImportantFeatInd(rsfEst,100)])
kmeansAcc = clusterAcc(kmeansEst, trainingData, trainingLabels)









