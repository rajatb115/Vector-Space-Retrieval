import os
from collections import defaultdict
import math
from datetime import datetime

# Function to compute current time
def get_current_time():
	now = datetime.now()
	return (now.strftime("%H:%M:%S"))

# Function to remove stopwords
def get_stopwords(stopwords_file):
    with open(stopwords_file, mode='r') as f:
        stopwords = set(f.read().split())
    return stopwords

# Function to get the documents
def get_docs(dataset_path):
    docs = []
    for doc_file in os.listdir(dataset_path):
        docs.append(os.path.join(dataset_path, doc_file))
    return docs

# Function to compute idf of each term in corpus
def compute_idf(corpus):
    num_docs = len(corpus)
    idf = defaultdict(lambda: 0)
    for doc in corpus:
        for word in doc.keys():
            idf[word] += 1

    for word, value in idf.items():
        idf[word] = math.log(1+(num_docs / value))
    return idf

# Function to compute weight of each term in the corpus
def compute_weights(idf, doc):
    for word, value in doc.items():
        doc[word] = idf[word] * (1 + math.log(value))

# Function to normalize the keywords
def normalize(doc):
    denominator = math.sqrt(sum([e ** 2 for e in doc.values()]))
    for word, value in doc.items():
        doc[word] = value / denominator
    
# Function to build inverted index
def build_inverted_index(idf, corpus, doc_id_list):
    inverted_index = {}
    for word, value in idf.items():
        inverted_index[word] = {}
        inverted_index[word]['idf'] = value
        inverted_index[word]['postings_list'] = []

    for index, doc in enumerate(corpus):
        for word, value in doc.items():
            inverted_index[word]['postings_list'].append([doc_id_list[index], value])
    return inverted_index
