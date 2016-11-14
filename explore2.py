import pandas as pd
import nltk
import re

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



def clean(hrc_data, bad_strings):
	hrc_copy = hrc_data.copy()
	for i in range(len(hrc_copy)):
		new_text = hrc_copy.iloc[i].text
		new_text = remove_beginning(new_text, i)
		for bad in bad_strings:
			new_text = re.sub(bad, "", new_text)
		hrc_copy.loc[i, "text"] = new_text
	return hrc_copy

cleaned = clean(hrc_train, bad_strings)


unclass = []
for i in range(len(cleaned)):
	if "unclassified u.s." in cleaned.iloc[i].text:
		unclass += [i]