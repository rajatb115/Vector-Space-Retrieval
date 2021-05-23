import sys
import os
import re
from collections import Counter
from nltk.tokenize import word_tokenize 
import nltk 
from datetime import datetime
import pickle
import math
from utils import textprocessing,helpers

# Loading resource files and the stopword file and save it as global variable.
resources_path = os.path.join(os.getcwd(), 'resources')
data_path = os.path.join(os.getcwd(), 'data')
stopwords_file = os.path.join(resources_path, 'stopwords_en.txt')
stopwords = helpers.get_stopwords(stopwords_file)


corpus=[]
doc_id_list = []

# Function to find the special tag words.
def find_fun(read,s,s1):
    res = [i for i in range(len(read)) if read.startswith(s, i)]
    res1 = [i for i in range(len(read)) if read.startswith(s1, i)]
    
    lis = []
    l1 = len(s)
    l2 = len(s1)
    
    temp = 0;
    name = ""
    for i in range(len(res)):
        if(temp==0):
            t = res[i]+l1
            t1 = res1[i]-1
            name =(textprocessing.remove_nonwords((read[t:t1]).lower())).strip()
            
            if(i+1!=len(res)):
                if(res[i+1]-1 - (res1[i]+l2)==0):
                    #print(":"+(clean_func(read[res[i]+l1:res1[i]-1])).strip().lower())
                    keyword = (textprocessing.remove_nonwords((read[res[i]+l1:res1[i]-1]).lower())).strip()
                    if(len(keyword)>0):
                        lis.append(keyword)
                    temp=1
                elif(res[i+1]-1 -(res1[i]+l2) ==1 and len(read[res1[i]+l2:res[i+1]-1].strip())==0):
                    #print(":"+(clean_func(read[res[i]+l1:res1[i]-1])).strip().lower())
                    keyword = (textprocessing.remove_nonwords((read[res[i]+l1:res1[i]-1]).lower())).strip()
                    if(len(keyword)>0):
                        lis.append(keyword)
                    temp=1
            if temp==0:
                name = textprocessing.remove_nonwords(name)
                name = (name.lower()).strip()
                if(len(name)>0):
                    lis.append(name)
                name=""
        else:
            t = res[i]+l1
            t1 = res1[i]-1
            
            name = (name+" "+textprocessing.remove_nonwords((read[t:t1]).lower()).strip()).strip()
            if(i+1!=len(res)):
                if(res[i+1]-1 - (res1[i]+l2)==0):
                    #print(":"+(clean_func(read[res[i]+l1:res1[i]-1])).strip().lower())
                    keyword = (textprocessing.remove_nonwords((read[res[i]+l1:res1[i]-1]).lower())).strip()
                    if(len(keyword)>0):
                        lis.append(keyword)
                    temp=1
                elif(res[i+1]-1 -(res1[i]+l2) ==1 and len(read[res1[i]+l2:res[i+1]].strip())==0):
                    #print(":"+(clean_func(read[res[i]+l1:res1[i]-1])).strip().lower())
                    keyword = (textprocessing.remove_nonwords((read[res[i]+l1:res1[i]-1]).lower())).strip()
                    if(len(keyword)>0):
                        lis.append(keyword)
                    temp=1
                else:
                    #print(":"+(clean_func(read[res[i]+l1:res1[i]-1])).strip().lower())
                    keyword = (textprocessing.remove_nonwords((read[res[i]+l1:res1[i]-1]).lower())).strip()
                    if(len(keyword)>0):
                        lis.append(keyword)
                    temp=0
            else:
                #print(":"+(clean_func(read[res[i]+l1:res1[i]-1])).strip().lower())
                keyword = (textprocessing.remove_nonwords((read[res[i]+l1:res1[i]-1]).lower())).strip()
                if(len(keyword)>0):
                    lis.append(keyword)
                temp=0
            
            if temp==0:
                name = textprocessing.remove_nonwords(name.lower())
                name = name.lower().strip()
                if(len(name)>0):
                    lis.append(name)
                name=""
    return lis

def check_data(read):
    #global variables
    global corpus
    global stopwords
    global doc_id_list
    
    # Finding the document name from each file
    t = read.find("<DOCNO>")+7
    t1 = read.find("/DOCNO")-1
    doc_id = (read[t:t1].strip())
    doc_id_list.append(doc_id)

    # combining text tag data if more than one text tag are present in the document
    res = [i for i in range(len(read)) if read.startswith("<TEXT>", i)]
    res1 = [i for i in range(len(read)) if read.startswith("</TEXT", i)]
    
    doc_text=""
    for i in range(len(res)):
        t = res[i]+6
        t1 = res1[i]-1
        doc_text = doc_text+" "+(read[t:t1].strip())
    
    
    # detecting the special tag words like person, organization and location.
    person = find_fun(doc_text,"<PERSON>","</PERSON>")
    doc_text =doc_text.replace("<PERSON>", "")
    doc_text =doc_text.replace("</PERSON>", "")
    
    organization = find_fun(doc_text,"<ORGANIZATION>","</ORGANIZATION>")
    doc_text =doc_text.replace("<ORGANIZATION>", "")
    doc_text =doc_text.replace("</ORGANIZATION>", "")
    
    location = find_fun(doc_text,"<LOCATION>","</LOCATION>")
    doc_text =doc_text.replace("<LOCATION>", "")
    doc_text =doc_text.replace("</LOCATION>", "")
    
    words = textprocessing.preprocess_text(doc_text, stopwords)
    bag_of_words = Counter(words)
    counts = Counter(person)
    
    for a in counts:
        bag_of_words["P:"+a]=counts[a]
    counts = Counter(location)
    
    for a in counts:
        bag_of_words["L:"+a]=counts[a]
    counts = Counter(organization)
    
    for a in counts:
        bag_of_words["O:"+a]=counts[a]
    
    corpus.append(bag_of_words)

# funtion to read file
def readfile_func(path_to_file):
    read = ""
    list_data=[]
    with open(path_to_file, 'r') as input:
        for line in input:
            if '</DOC>' in line:
                read = read + ("</DOC>")
                check_data(read)
                read = ""
            read = read + line

def main(argv):
    # global variables
    global corpus
    global doc_id_list
    
    # Checking If arguments are not proper
    if(len(argv)!=2):
        print("--> Please check your command format\n--> Format : python3 invidx_cons.py <path> <index file name>\n")
        return
    
    # If arguments are proper we will do the further processing
    out_file = argv[1]
    path_dir = argv[0]
    
    for file in os.listdir(path_dir):
        
        current_time = helpers.get_current_time()
        print("Analysing file : "+path_dir+"/"+file +" (Start Time = "+current_time+" )")
        
        
        readfile_func(path_dir+"/"+file)
        
        
        current_time = helpers.get_current_time()
        print("Analysing of file : "+path_dir+"/"+file+" completed ..."+" (End Time = "+current_time+" )")
        
    idf = helpers.compute_idf(corpus)
    
    # finding normailised tf-idf for each word in the corpus
    for doc in corpus:
        helpers.compute_weights(idf,doc)
        helpers.normalize(doc)
    
    
    # Bulding inverted index
    print("building inverted index ...")
    current_time = helpers.get_current_time()
    print("Building inverted index started at "+current_time)
    
    inverted_index = helpers.build_inverted_index(idf, corpus, doc_id_list)
    
    current_time = helpers.get_current_time()
    print("Building inverted index completed at "+current_time)
    
    
    # writing data to file
    
    print("Writing data to files ...")
    current_time = helpers.get_current_time()
    print("Writing data in files started at "+current_time)
    
    file_key = open(out_file+".dict","w")
    
    file_postings = open(out_file+".idx","wb")
    
    
    for word in idf.keys():
        file_key.write(word + '\n')
    
    for i in inverted_index.items():
        pickle.dump(i,file_postings)
        
        
    file_key.close()
    file_postings.close()
    
    current_time = helpers.get_current_time()
    print("Writing data in files completed at "+current_time)
    
# main function
if __name__ == "__main__":
    print("indexing Data.....")
    main(sys.argv[1:])