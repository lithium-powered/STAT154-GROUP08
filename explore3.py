import pandas as pd
import nltk
import re
from collections import Counter
import numpy as np

hrc_train = pd.read_csv("HRC_train.tsv", sep = "\t", header = None, )

bad_strings = ["unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. release in full from ,  d <cd@state.gov " , " unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state..........." , "unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. release in part b. ","unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state...........", "unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver.", "unclassified u.s. department of state case no. ............ doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state........... ","unclassified u.s. department of state case no. ............ doc no. c........ date: .......... ","unclassified u.s. department of state case no. ............ doc no. c........ state dept. . produced to house select benghazi comm. date: .......... subject to agreement on sensitive information & redactions. no foia waiver. state...........", " unclassified u.s. department of state case no. ............. doc no. c........ date: .......... state dept. . produced to house select benghazi comm. subject to agreement on sensitive information & redactions. no foia waiver. state...........", "unclassified u.s. department of state case no ............ doc no c........ state dept . produced to house select benghazi comm date .......... subject to agreement on sensitive information & redactions no foia waiver state...........","unclassified u.s. department of state case no ............ doc no c........ date .......... subject to agreement on sensitive information & redactions no foia waiver state........... state dept. . produced to house select benghazi comm.", "unclassified u.s. department of state case no ............ doc no. c........ date: ..........","unclassified u.s. department of state case no ............ b. b. b. doc no. c........ state dept. . produced to house select benghazi comm. date: .......... subject to agreement on sensitive information & redactions. no foia waiver. state...........", "unclassified u.s. department of state case no:............ doc no. c........ date: ..........", "unclassified u.s. department of state base no. ............ doc no. c........ date: ..........", "unclassified u.s. department of state case no. . ............ doc no. c........ date: ..........", "unclassified u.s. department of state case no. ' ............ doc no. c........ date: ..........","unclassified u.s. department of state case no. ............. doc no. c........ date: ..........", "unclassified u.s. department of state case no. ............... doc no. c........ date: ..........","unclassified u.s. department of state case no............. doc no. c........ date: ..........","unclassified u.s. department of state case no............ doc no. c........ date: ..........","unclassified u.s. department of state case no................... doc no. c........ date: ..........", "unclassified u.s. department of state case no. .............. doc no. c........ date: ..........", "unclassified u.s. department of state case no. ................ doc no. c........ date: ..........","unclassified u.s. department of state case no................ doc no. c........ date: ..........","unclassified u.s. department of state case no............... doc no. c........ date: ..........", "unclassified u.s. department of state case no. ............ doc no. c........ date: ..........","unclassified u.s. department of state case no. ............", "doc no. c........ date: ..........", "unclassified u.s. department of state case no ............"," unclassified u.s. department of state case ................", " unclassified u.s. department of state case no.............."] 

def remove_beginning(text, i):
	try:
		j = text.index("sent")
		new = text[j:]
		return new
	except ValueError:
		print("sent not found in row ", str(i))
		return text

def find_string(df, text):
    senders = []
    indices = []
    for i in range(len(df)):
        if text in df.iloc[i].text.split():
            senders += [get_sender(df, i)]
            indices += [i]
    print(text, " found in emails:", indices)
    return senders

phone1 = find_string(hrc_train, "202-647-9533")
print(Counter(phone1))
