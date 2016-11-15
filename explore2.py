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

def remove_punctuation(text):
	text = re.sub("-", " ", text)
	text = re.sub("["+string.punctuation+"]", "", text)
	text = re.sub("\\\\", "", text)
	return text


def clean(hrc_data, bad_strings):
	hrc_copy = hrc_data.copy()
	for i in range(len(hrc_copy)):
		new_text = hrc_copy.iloc[i].text
		new_text = remove_beginning(new_text, i)
		for bad in bad_strings:
			new_text = re.sub(bad, "", new_text)
		new_text = remove_punctuation(new_text)	
		new_text = stop_and_stem(new_text)
		hrc_copy.loc[i, "text"] = new_text
	return hrc_copy

cleaned = clean(hrc_train, bad_strings)



def unique(df):
	word_list = []
	for i in range(len(df)):
		word_list += df.iloc[i].text.split()
	return list(set(word_list))



uniques = unique(cleaned)
print "There are ", len(uniques), " unique words."

def get_sender(df, index):
	return df.iloc[index].id

def counts(text):
	return Counter(text.split())


def feature_matrix(df, unique_words):
	dict_list = []
	for i in range(len(df)):
		dict_list += [counts(df.iloc[i].text)]
	fm = pd.DataFrame(dict_list)	
	fm = fm.fillna(value=0).astype(dtype=int)
	return fm

fm = feature_matrix(cleaned, uniques)
fm.shape
fm.head()

#fm.to_csv("test.csv") 