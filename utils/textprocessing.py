import re
from nltk.stem.porter import PorterStemmer

# Remove the non words.
def remove_nonwords(text):
    non_words = re.compile(r"[^a-z ]")
    processed_text = re.sub(non_words, '', text)
    return processed_text.strip()
    
def remove_nonwords_ex1(text):
	non_words = re.compile(r"[^a-z* ]")
	processed_text = re.sub(non_words, '', text)
	return processed_text.strip()

# Function to remove the stop words from the list of the vocabulary.
def remove_stopwords(text, stopwords):
    words = [word for word in text.split() if word not in stopwords]
    return words

# Function to pre-process the text
def preprocess_text(text, stopwords):
    processed_text = remove_nonwords(text.lower())
    words = remove_stopwords(processed_text, stopwords)
    return words
