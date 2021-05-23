import sys
import pickle
import math
import os
from pytrie import StringTrie
from utils import textprocessing
from utils import helpers
from collections import Counter
from pathlib import Path


# prefix search function for words ending with *
def prefixSearch(arr,prefix):
    # create empty trie 
    trie=StringTrie() 
    for key in arr: 
        trie[key] = key 
    return trie.values(prefix)


def main(argv):
    cutoff = 100
    queryfile = ""
    indexfile = ""
    resultfile=""
    dictfile = ""
    
    # Checking commandline arguments
    if(len(argv)>=2):
        if argv[0] == "--query":
            queryfile = argv[1]

        if argv[0]=="--cutoff":
            cutoff = argv[1]

        if(argv[0]== "--index"):
            indexfile = argv[1]

        if argv[0]=="--dict":
            dictfile = argv[1]
        
        if argv[0]=="--output":
            resultfile = argv[1]
    if(len(argv)>=4):
        if argv[2] == "--query":
            queryfile = argv[3]

        if argv[2]=="--cutoff":
            cutoff = argv[3]

        if(argv[2]== "--index"):
            indexfile = argv[3]

        if argv[2]=="--dict":
            dictfile = argv[3]
        
        if argv[2]=="--output":
            resultfile = argv[3]
    
    if(len(argv)>=6):
        if argv[4] == "--query":
            queryfile = argv[5]

        if argv[4]=="--cutoff":
            cutoff = argv[5]

        if(argv[4]== "--index"):
            indexfile = argv[5]

        if argv[4]=="--dict":
            dictfile = argv[5]
        
        if argv[4]=="--output":
            resultfile = argv[5]
        
    if(len(argv)>=8):
        if argv[6] == "--query":
            queryfile = argv[7]

        if argv[6]=="--cutoff":
            cutoff = argv[7]

        if(argv[6]== "--index"):
            indexfile = argv[7]

        if argv[6]=="--dict":
            dictfile = argv[7]
        
        if argv[6]=="--output":
            resultfile = argv[7]
        
    if(len(argv)>=10):
        if argv[8] == "--query":
            queryfile = argv[9]

        if argv[8]=="--cutoff":
            cutoff = argv[9]

        if(argv[8]== "--index"):
            indexfile = argv[9]

        if argv[8]=="--dict":
            dictfile = argv[9]
        
        if argv[8]=="--output":
            resultfile = argv[9]
    
    # Checking the command line argument.
    if(queryfile == ""):
        print("--> Please check your command format\n--> Format : python3 vecsearch.py --query <queryfile> --cutoff <k> --output <resultfile> --index <indexfile> --dict <dictfile>\n")
        return
    if(indexfile == ""):
        print("--> Please check your command format\n--> Format : python3 vecsearch.py --query <queryfile> --cutoff <k> --output <resultfile> --index <indexfile> --dict <dictfile>\n")
        return
    if(dictfile == ""):
        print("--> Please check your command format\n--> Format : python3 vecsearch.py --query <queryfile> --cutoff <k> --output <resultfile> --index <indexfile> --dict <dictfile>\n")
        return
    if resultfile == "":
        print("--> Please check your command format\n--> Format : python3 vecsearch.py --query <queryfile> --cutoff <k> --output <resultfile> --index <indexfile> --dict <dictfile>\n")
        return
    if (int(cutoff)<=0):
        print("plase check the cutoff value it should be greater than 0")
        return
    
    # Checking if all files exist or not
    print("Checking files ...")
    
    my_path = Path(resultfile)
    if my_path.exists():
        print("Output file already exist.")
        print("Deleting output file and new output file will be created.")
        os.remove(resultfile)
    else:
        print("Output file doesn't exist. New output file will be created.")
    
    my_path = Path(queryfile)
    if my_path.exists():
        print("Query file exist...")
    else:
        print("Query file doesn't exist... Please provide correct path... Returning")
        return
    
    my_path = Path(indexfile)
    if my_path.exists():
        print("Index file exist...")
    else:
        print("Index file doesn't exist... Please provide correct path... Returning")
        return
    
    my_path = Path(dictfile)
    if my_path.exists():
        print("Dict file exist...")
    else:
        print("Dict file doesn't exist... Please provide correct path... Returning")
        return
    
    number = []
    query_list = []
    # reading query file for the query
    with open(queryfile, 'r') as rf:
        for line in rf:
            if '<num>' in line:
                data = line.strip().split("Number:")
                number.append(data[1].strip())
                
            if '<title>' in line:
                data = line.strip().split("Topic:")
                query_list.append((data[1].strip()))
    
    # reading the vocabulary from dictfile
    vocab = []
    with open(dictfile,'r') as rf:
        for line in rf:
            vocab.append(line.strip())
    
    # Reading inverted index and storing in dictonary
    dict_file = open(indexfile,'rb')
    inverted_index = {}
    while 1:
        try:
            get_word = pickle.load(dict_file)
            inverted_index[get_word[0]]=get_word[1]
        except (EOFError, pickle.UnpicklingError):
            break
    dict_file.close()
    
    # Removing stopwords from our query
    stopwords_file = os.path.join(os.getcwd(), 'resources', 'stopwords_en.txt')
    stopwords = helpers.get_stopwords(stopwords_file)
    
    # Processing each query and finding the relevent document from the corpus
    for i in range (len(number)):
        
        query = ""
        query_ex = query_list[i]
        
        # to check special word (like location, organization and person) or prefix search or combination of special word and prefix search
        for query_word in query_ex.split():
            if len(query_word)>2 and query_word[1]==":":
                prefix_letter = ""
                if(query_word[0]=="O" or query_word[0]=="P" or query_word[0]=="L"):
                    prefix_letter =query_word[:2]
                    if(query_word[len(query_word)-1]=="*" and len(query_word[2:len(query_word)-1])==len(textprocessing.remove_nonwords((query_word[2:len(query_word)-1]).lower()))):
                        search_word = prefix_letter + (query_word[2:len(query_word)-1]).lower()
                        lis = prefixSearch(vocab,search_word)
                        print("lis = "+str(lis))
                        for lis_word in lis:
                            query=query+" "+lis_word
                    else:
                        query = query + " "+textprocessing.remove_nonwords(query_word.lower())
                else:
                    query = query + " "+ textprocessing.remove_nonwords(query_word.lower())
            else:
                if(query_word[len(query_word)-1]=="*" and len(query_word[:len(query_word)-1])==len(textprocessing.remove_nonwords((query_word[:len(query_word)-1]).lower()))):
                    query_word = textprocessing.remove_nonwords((query_word[:len(query_word)-1]).lower())
                    lis = prefixSearch(vocab,query_word)
                    for lis_word in lis:
                        query=query+" "+lis_word
                else:
                    query = query +" "+ textprocessing.remove_nonwords(query_word.lower())
        
        query = textprocessing.remove_stopwords(query.strip(), stopwords)
        query = [word for word in query if word in vocab]
        query = Counter(query)
        
        # Compute the weight of the words in the query
        for word, value in query.items():
            query[word] = inverted_index[word]['idf'] * (1 + math.log(value))
        
        # Normalizing the words in the query
        helpers.normalize(query)
        
        scores={}
        # Searching posting list regarding the words in the query and finding the weight of the document
        for word, value in query.items():
            for doc in inverted_index[word]['postings_list']:
                doc_name, weight = doc
                if str(doc_name) in scores.keys():
                    scores[str(doc_name)] += value * weight
                else:
                    scores[str(doc_name)] = value * weight
        
        
        scores_list = []
        for key, value in scores.items():
            temp = [value,key]
            scores_list.append(temp)
        
        scores_list.sort(reverse=True)
        
        # writing the output file
        result_file = open(resultfile,'a')
        for ii in range(len(scores_list)):
            if(ii<int(cutoff)):
                result_file.write(str(str(int(number[i]))+" 0 "+str(scores_list[ii][1])+" "+str(ii+1)+" "+str(scores_list[ii][0])+" STANDARD\n"))
            else:
                break
        
        result_file.close()
        
    print("Output file created successfully....")

# main function
if __name__=="__main__":
    main(sys.argv[1:])