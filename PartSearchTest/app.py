from flask import Flask, render_template,request,redirect,url_for
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import re
from csv import reader
from fuzzywuzzy import fuzz, process

app = Flask(__name__)

@app.route('/')
def homePage():
    return render_template("partSearch.html")

@app.route('/getSearchResult',methods = ['POST', 'GET'])
def getSearchResult():
    if request.method == 'POST':
        Search = request.form['Search']
        my_dict = CalculatedSearchData(Search);
        
        print ("Search Result", my_dict)
        return render_template("partSearch.html",my_dict=my_dict)
        #return redirect(url_for('homePage',my_dict=my_dict))


stopwords = set(stopwords.words("english"))

    #Master Data
dictionary = pd.read_csv('E:\JS\Py\Text_similarity\Fuzzy.csv', header=None, squeeze=True).to_dict()
    
    #Second Master Data
with open('E:\JS\Py\Text_similarity\Second_dict.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    sec_dict = list(map(tuple, csv_reader))

master_doc = []
match_doc = []
#using Lemmatization
lemma = nltk.wordnet.WordNetLemmatizer()


test_doc = []
test_line = []
 # create a clean document after removing the stop-words and generate lemmas
clean_doc = []

final_doc=[]

def stringsearch(string, sub_str, sub_str1, line):
    if(string.find(sub_str)!=-1 and string.find(sub_str1)!=-1):
        final_doc.append(sub_str+" "+sub_str1)
        return (1)
        
def secondsearch(string, sub_str, line):
    r = fuzz.token_set_ratio(string, sub_str)
    #r = fuzz.token_sort_ratio(string, sub_str)
    if(r > 90):
        final_doc.append(sub_str)        
        return (1)

def listtostring(clean_line):
    return(" ".join(clean_line))

def replacer(string1):
    return(string1.replace('\bscr\b','screw').replace('\bspr\b','spring').replace('\bbd\b','band').replace('spr bd','spring band').replace('spr.','spring').replace('separator','clamp').replace('assembly','assy')
           .replace('\bw/h\b','wiring harness').replace('brg','bearing').replace('bkt','bracket').replace('\bwh\b','wiring harness').replace('\bbso\b','body side outer').replace('pigtail','pigtail wiring harness')
           .replace('w/h','wiring harness').replace('\breinf\b','reinforcement').replace('wh','wiring harness').replace('mtg.','mounting').replace('ccb','cross car beam').replace('\bais\b','air intake system')
           .replace('\bmtg\b','mounting').replace('\bbrkt\b','bracket').replace('\brr\b','rear').replace('frt','front').replace('\bdr\b','door').replace('engine cooling system','radiator').replace('\bra\b','rear axle')
           .replace('reinfrocement','reinforcement').replace('mountingbracket','mounting bracket').replace('nylon pipe','nylon bunch').replace('pipe bunch','nylon bunch').replace('vent tube','vent hose').replace('\bvent\b','ventilation')
           .replace('suction tube','suction hose').replace('\bcyl\b','cylinder').replace('clutch line','clutch hose').replace('suction pipe','suction hose').replace('suction line','suction hose').replace('fuel return pipe','fuel return hose')
           .replace('clutch pipe','clutch hose').replace('coolant pipe','coolant hose').replace('exh','exhaust').replace('batt','battery').replace('loadbody','load body').replace('\barb\b','anti roll bar').replace('window regulator','window winding')
           .replace('pressure line','pressure hose').replace('return line','return hose').replace('gear box','gearbox').replace('shell assy','load body').replace('\bfl\b','flanged').replace('flat bed','load body').replace('high deck','load body')
           .replace('lining','liner').replace('\bgb\b','gearbox').replace('\bstg\b','steering').replace('-conn','connector').replace('\bconn\b','connector').replace('washer tank','washer bottle'))
   

test_line = []
def CalculatedSearchData(SearchData):
    global final_doc
    clean_doc =[]    
    test_line =[]
    file_docs = []
    file_docs.append(SearchData)
    my_dict = {}
    for line in file_docs:
        clean_line = [word for word in line.split() if word not in stopwords]        
        for word in line.split():
            test_line.append(lemma.lemmatize(word))
        test_doc.append(listtostring(test_line))
        #clean_doc.append(listtostring(clean_line))
        clean_doc = test_doc
    
    init_size = len(clean_doc)
    print ("SSIZe ", init_size);    
    ##first loop of search and filtering
    for line in clean_doc:    
        line1 = line.lower()
        string = line1.partition(",")[0].partition(";")[0].partition("(")[0].partition("[")[0].partition('for')[0].partition('with')[0].partition('w/o')[0].partition('offer')[0].partition('\bw\b')[0]
        for y in sec_dict:
            #print ("clean_doc ", replacer(string.lower()),y[0].lower(),y[1].lower(), line);
            #print ("Result ", stringsearch(replacer(string.lower()),y[0].lower(),y[1].lower(), line));
            if (stringsearch(replacer(string.lower()),y[0].lower(),y[1].lower(), line) == 1):                
                #print(line, " Stage 1  is ::-->")
               
                clean_doc.remove(line)
                break
        if(len(final_doc)!=0):
            #print(final_doc)
            my_dict = {'PART NAME': line, 'Mach Data': final_doc[0]}
        final_doc = [] 

    ##second loop of search and filtering (fuzzy search)
    for line in clean_doc:    
        line1 = line.lower()
        string = line1.partition(",")[0].partition(";")[0].partition("(")[0].partition("[")[0].partition('for')[0].partition('with')[0].partition('w/o')[0].partition('offer')[0].partition('\bw\b')[0]

        for x in dictionary:        
            if (secondsearch(replacer(string.lower()),dictionary[x].lower(), line) == 1):
                #print(line, "Stage 2 is ::-->")
                clean_doc.remove(line)
                break            
        if(len(final_doc)!=0):
            #print(final_doc)
            my_dict = {'PART NAME': line, 'Mach Data': final_doc[0]}
        final_doc = []
    
    if not bool(my_dict):
        my_dict = {'PART NAME': line, 'Mach Data': 'Match Not Found '}    
    return my_dict
   


if __name__ == '__main__':
    app.run(debug = True) 