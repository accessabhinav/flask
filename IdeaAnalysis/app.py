from flask import Flask, render_template,request,redirect,url_for
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import re, os, csv
from csv import reader
from fuzzywuzzy import fuzz, process
from werkzeug.utils import secure_filename
import gensim


UPLOAD_FOLDER = 'C:/Users/CORE i3/Anaconda3/envs/Uploaded_files'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def homePage():
    return render_template("ideaSearch.html")


@app.route('/getSearchResult',methods = ['POST', 'GET'])
def getSearchResult():
    temp_doc = []
    if request.method == 'POST':
        file = request.files['csvfile']
        #ideaSearch = request.form['search']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        name = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        #return redirect(url_for('uploaded_file', filename=file.filename))
        
        file_path = UPLOAD_FOLDER + "/" + name
        with open(file_path, 'r', encoding="UTF-8") as inp, open(UPLOAD_FOLDER + "/wup.txt", 'w') as out:
            for line in inp:
                out.write(line + '.\n')

        with open (UPLOAD_FOLDER + "/wup.txt") as f:
            tokens = sent_tokenize(f.read())
            for line in tokens:
                temp_doc.append(line)
        
        my_dict = CalculatedSearchData(temp_doc);
        
        return render_template("ideaSearch.html",my_dict=my_dict)
        
stopwords = set(stopwords.words("english"))

master_doc = []
match_doc = []
#using Lemmatization
lemma = nltk.wordnet.WordNetLemmatizer()


test_doc = []
test_line = []
clean_doc = []

final_doc=[]

def listtostring(clean_line):
    return(" ".join(clean_line))

test_line = []
def CalculatedSearchData(SearchData):
    global final_doc
    clean_doc =[]    
    test_line =[]
    file_docs = []
    test_doc = []
    file2_docs = SearchData
    my_dict = {}

    with open ('E:\JS\Py\Text_similarity\Idea_List1.txt') as f:
        tokens = sent_tokenize(f.read())
    
    for line in tokens:
        file_docs.append(line)
        
# create a clean document after removing the stop-words and generate lemmas
   
    clean_doc = []
    for line in file_docs:
        clean_line = [word for word in line.split() if word not in stopwords]
        
        for word in line.split():
            test_line.append(lemma.lemmatize(word))
        test_doc.append(listtostring(test_line))
        test_line = []
        
        #clean_doc.append(listtostring(clean_line))
        clean_doc = test_doc

    #print("Number of documents:",len(clean_doc))

    gen_docs = [[w.lower() for w in word_tokenize(text)] 
                for text in clean_doc]

    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    tf_idf = gensim.models.TfidfModel(corpus)

    # building the index
    sims = gensim.similarities.Similarity('E:/JS/Py/Text_similarity/', tf_idf[corpus], num_features=len(dictionary))

    test_doc = []
    clean_doc2 = []
    for line in file2_docs:
        clean_line = [word for word in line.split() if word not in stopwords]
        
        for word in line.split():
            test_line.append(lemma.lemmatize(word))
        test_doc.append(listtostring(test_line))
        test_line = []
        
        clean_doc2 = test_doc

    #print("\nNumber of documents:",len(clean_doc2))
        
    #new_doc = [line.lower() for line in clean_doc]
    limit = 5
    for line in clean_doc2:
        sim_score = process.extract(line.lower(), clean_doc, scorer=fuzz.token_sort_ratio, limit = limit)
        
        my_dict[line] = sim_score
        
    return my_dict


if __name__ == '__main__':
    app.run(debug = True) 