import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
from collections import Counter
import numpy as np

hrc_train = pd.read_csv("HRC_train.tsv", sep="\t", header=None, names=["id", "text"])


bad_strings = ["unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. release in full from ,  d <cd@state.gov " , " unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state..........." , "unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. release in part b. ","unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state...........", "unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver.", "unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state........... ","unclassified u.s. department of state case no. ............ doc no. c........ date: .......... ","unclassified u.s. department of state case no. ............ doc no. c........ state dept. . produced to house select benghazi comm. date: .......... subject to agreement on sensitive information & redactions. no foia waiver. state...........", " unclassified u.s. department of state case no. ............. doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state...........", "unclassified u.s. department of state case no ............ doc no c........ state dept . produced to house select benghazi comm date .......... subject to agreement on sensitive information & redactions no foia waiver state...........","unclassified u.s. department of state case no ............ doc no c........ date .......... subject to agreement on sensitive information & redactions no foia waiver state........... state dept. . produced to house select benghazi comm.", "unclassified u.s. department of state case no ............ doc no. c........ date: ..........","unclassified u.s. department of state case no ............ b. b. b. doc no. c........ state dept. . produced to house select benghazi comm. date: .......... subject to agreement on sensitive information & redactions. no foia waiver. state...........", "unclassified u.s. department of state case no:............ doc no. c........ date: ..........", "unclassified u.s. department of state base no. ............ doc no. c........ date: ..........", "unclassified u.s. department of state case no. . ............ doc no. c........ date: ..........", "unclassified u.s. department of state case no. ' ............ doc no. c........ date: ..........","unclassified u.s. department of state case no. ............. doc no. c........ date: ..........", "unclassified u.s. department of state case no. ............... doc no. c........ date: ..........","unclassified u.s. department of state case no............. doc no. c........ date: ..........","unclassified u.s. department of state case no............ doc no. c........ date: ..........","unclassified u.s. department of state case no................... doc no. c........ date: ..........", "unclassified u.s. department of state case no. .............. doc no. c........ date: ..........", "unclassified u.s. department of state case no. ................ doc no. c........ date: ..........","unclassified u.s. department of state case no................ doc no. c........ date: ..........","unclassified u.s. department of state case no............... doc no. c........ date: ..........", "unclassified u.s. department of state case no. ............ doc no. c........ date: ..........","unclassified u.s. department of state case no. ............", "doc no. c........ date: ..........", "unclassified u.s. department of state case no ............"," unclassified u.s. department of state case ................", " unclassified u.s. department of state case no.............."] 



def remove_beginning(text, i):
	try:
		j = text.index("sent")
		new = text[j:]
		return new
	except ValueError:
		print "sent not found in row " + str(i)
		return text


sno = nltk.stem.SnowballStemmer('english')
stop = set(stopwords.words('english'))
def stop_and_stem(string):
	#tokenize
	words = string.split()
	#remove stop words
	word_list = [i  for i in words if i not in stop]
	#stemming
	word_list = [sno.stem(i) for i in word_list]
	new_text = " ".join(word_list)
	return new_text

def clean(hrc_data, bad_strings):
	hrc_copy = hrc_data.copy()
	for i in range(len(hrc_copy)):
		new_text = hrc_copy.iloc[i].text
		new_text = remove_beginning(new_text, i)
		for bad in bad_strings:
			new_text = re.sub(bad, "", new_text)
		new_text = re.sub("-", " ", new_text)
		new_text = re.sub("["+string.punctuation+"]", "", new_text)
		new_text = re.sub("\\\\", "", new_text)
		new_text = stop_and_stem(new_text)
		hrc_copy.loc[i, "text"] = new_text
	return hrc_copy

cleaned = clean(hrc_train, bad_strings)



def unique(df):
	uniques = []
	sno = nltk.stem.SnowballStemmer('english')
	for i in range(len(df)):
		word_list = df.iloc[i].text.split()
		uniques += word_list
	return list(set(uniques))



a = unique(cleaned)
print "length of a = ", len(a)

def get_sender(df, index):
	return df.iloc[index].id

def counts(text, unique_words):
	words = text.split()
	wordCount = Counter(words)
	return wordCount


def feature_matrix(df, unique_words):
	fm = np.zeros((len(df), len(unique_words)))
	for i in range(len(df)):
		wordCount = counts(df.iloc[i].text, unique_words)
		for j in range(len(unique_words)):
			try:
				fm[i][j] = wordCount[unique_words[j]]
			except KeyError:
				fm[i][j] = 0

	return fm


test = feature_matrix(cleaned, a)
Y = numpy.asarray[get_sender(cleaned, i) for i in range(3505)])

numpy.savetxt("trainingData.csv",a, delimiter=",")
numpy.savetxt("trainingLabel.csv",a,delimiter=",")