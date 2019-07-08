## Pre-processing

This folder contains the code relating to the processing of all the documents, as well as the highlights. My own functions are all written in *pre_processing_functions.py*. The pdfannots.py code was borrowed from Andrew Baumann and is used to extract highlights from pdfs:

https://github.com/0xabu/pdfannots

The functions are all called in extract highlights and process the documents is done in *extract highlights and process the documents.ipynb*. Furthermore, stop words are used from the following source:

https://eikhart.com/blog/dutch-stopwords-list

A list of employee names as stated in the system is saved in *names.txt* to remove these xml tags from the processed text.
