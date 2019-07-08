#External packages

from bs4 import BeautifulSoup
from nltk import SnowballStemmer
from tika import parser
from bs4 import BeautifulSoup
from string import punctuation
import nltk
import re
import io
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import itertools
from nltk.corpus import stopwords
import pandas as pd

#Importing the names and stop words to remove when processing the text
names_txt = os.getcwd().split('Master-Thesis')[0].replace('\\', '/') + 'Master-Thesis/research/pre-processing/names.txt'
all_no_words = []
nl_stopwords = stopwords.words('dutch')
names = open(names_txt,"r").read().split('\n')
all_no_words.append(names)
all_no_words.append(nl_stopwords)
all_no_words.append(['markering'])
all_no_words = list(itertools.chain.from_iterable(all_no_words))
all_names_markering = []
all_names_markering.append(['markering'])
all_names_markering.append(names)
all_names_markering = list(itertools.chain.from_iterable(all_names_markering))

'''Functions'''

#Tokenisation function
def process_input(page):
	return [re.sub(r'[^\w\s]','',w).replace('_','') for w in nltk.word_tokenize(page.lower())\
            if re.sub(r'[^\w\s]','',w).replace('_','') != '']

#Dutch stopword removal, from https://eikhart.com/blog/dutch-stopwords-list
def remove_stopwords(tokens):
	return [word for word in tokens if word not in all_no_words]

# Removes names from employee highlights from the processed text
def remove_names(tokens):
	return [word for word in tokens if word not in all_names_markering]

#Stems all the words using the NLTK snowball stemmer
def stemmer(tokens):
	stemmer = SnowballStemmer("dutch")
	return [stemmer.stem(token) for token in tokens]     

#Parser for the pdf documents and splits them on page level
def pdfminer_parser(path):
	rsrcmgr = PDFResourceManager()
	retstr = io.StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	fp = open(path, 'rb')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	password = ""
	maxpages = 0
	caching = True
	pagenos = set()
	pages = []

	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
								  password=password,
								  caching=caching,
								  check_extractable=True):
		interpreter.process_page(page)
		data = retstr.getvalue()
		pages.append(data)
		data = ''
		retstr.truncate(0)
		retstr.seek(0)
		
	return pages

#Takes as input the df and as output returns a dict with id:(text, label)
# for all the pages. The label is either true or false (contains a highlight or not)
def process_docs_and_label(df_anno, path_aktes,all_files):
	
	file_dict = {}
	dataframe = df(columns=['filename', 'text_tokenized', 'text_normal', 'page', 'norm_page', 'relevant'])

	for j, file in enumerate(all_files):     
		path = path_aktes + '/' + file
        
		split_page_doc = pdfminer_parser(path) 
		split_page_doc_soup = [BeautifulSoup(page, 'html.parser').get_text() for page in split_page_doc]
		annotated_pages = list(df_anno['page'].loc[df_anno['file'] == file])

		if (j+1) % 10 == 0:
			print(str(j+1) + ' processed out of ' + str(len(set(df_anno['file']))) + ' documents!')

		for i,page in enumerate(split_page_doc_soup):
				dataframe_2 = df({'filename': [file], 'text_tokenized': [stemmer(remove_stopwords(process_input(page)))], \
                                  'text_normal' : [page], 'page': [i+1], 'norm_page': [(i+1)/len(split_page_doc_soup)],   \
                                  'relevant': [(i+1) in set(annotated_pages)]})
                
				dataframe = dataframe.append(dataframe_2)

	return dataframe

    

#Extracts the year from the filename    
def extract_year(row):
    try:
        return re.search('\d{4}-\d{2}-\d{2}',row).group()[:4]
    except:
        return 'No year'
    
        
#Checks the highlight whether it relates to the zoning plan based on a set of rules
def remove_inconsistencies(row):
    
    #check if page has highlight
    
    if row['relevant'] == True:
        
        # Remove digits such as adress
        annotations =  ''.join(process_input(' '.join([i for i in row['text_anno'] if not i.isdigit()])))
        sentences = ''.join(process_input(' '.join([i for i in row['text_normal'] if not i.isdigit()])))
        
        # Decisive words for when len(list_indices) > 2 
        indicator_words = ['bijzondere', 'bepaling', 'besluit', 'bestemming', 'bestem']
        descriptions = ['tuin', 'souteraine', 'balkon', 'garage', 'berging', 'woning']
        
        # Counts the amount of times the highlighted text without numbers occurs in text
        list_indices = [m.start() for m in re.finditer(annotations, sentences)]
        if len(list_indices) >= 1:
           
            # Highlight gemeente amsterdam delete, too inconsistent when highlighted
            if ('gemeente' in annotations) and len(annotations) <=(len('gemeenteamsterdam')+2):
                return False

            # If highlight is unique or contains indicatorword, they are also always relevant
            elif any(re.findall(n,sentences) for n in indicator_words) == 1 and len(list_indices)==1:
                return True
            

            # Attempts to make the distinction between descriptions and usage
            elif len(list_indices) == 2:

                if any(re.findall(n,annotations) for n in descriptions): #check description words

                    if any(re.findall(n,sentences) for n in indicator_words): #check judicial terms
                        return True

                    else:
                        return False

                return True           

            # All highlighted text which occur 3 or more times are not relevant. Elimates doubles,
            # descriptions and highlights which are only different because of digits.

            elif len(list_indices) >= 3:
                return False
            
        elif any(re.findall(n,annotations) for n in indicator_words) and len(list_indices) == 0:
            return True
        else:
            return False
    else:
        return False
    return False