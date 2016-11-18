import numpy as np
import math
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score



def getRFEst(n_est, max_feat):
	rf = RandomForestClassifier(n_estimators = n_est, max_features = max_feat)
	return rf


def getCV(estimator, data, labels):
	return np.mean(cross_val_score(estimator, data, labels, cv = 5))


def getBestRFParam(data, labels):
	minCV = math.inf
	minParam = [1,10]
	for n_est in range(1,3000):
		for max_feat in range(10,2000):
			rf = getRFEst(n_est, max_feat)
			cv = getCV(rf, data, labels)
			if cv < minCV:
				minCV = cv
				minParam = [n_est, max_feat]
	return minParam


def getSVMEst(c):
	return svm.SVC(C = c)

def getBestSVMParam(data, labels):
	minCV = math.inf
	minParam = 0
	for c in range(0,10000):
		svm = getSVMEst(c)
		cv = getCV(svm, data, labels)
		if cv < minCV:
			minCV = cv
			minParam = c
	return minParam

def Kcluster(data):
	kmeans = KMeans(n_clusters = 5)
	kmeans.fit(data)
	return kmeans
