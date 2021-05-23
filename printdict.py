import os
import sys
import pickle

def main(argv):
    # Checking If arguments are not proper
    if(len(argv)!=1):
        print("--> Please check your command format\n--> Format : python3 printdict.py <file name>\n")
        return
    
    # If arguments are proper we will do the further processing
    
    
    st = argv[0].split(".")
    file_st = st[0]+".idx"
    
    if (os.path.exists(file_st)):
        
        read_file = open(file_st,"rb")
        lists=[]
        while 1:
            try:
                tll = read_file.tell()
                k = pickle.load(read_file)
                
                print(k[0],":",len(k[1]["postings_list"]),tll)
            except (EOFError, pickle.UnpicklingError):
                break
        read_file.close()
    else:
        print("No file exist with this name please check the file name.")

# Main function
if __name__ == "__main__":
    main(sys.argv[1:])