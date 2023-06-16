import nltk
from nltk.tokenize import word_tokenize
import sys
import os
import string
import math
from nltk.corpus import stopwords
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = {} # dictionary to store the file name and its contents
    for file in os.listdir(directory): # iterate through the files in the directory
        with open(os.path.join(directory, file) , encoding= "utf-8") as f: # open the file usnig utf-8 encoding which is the most common encoding for text files
            dic[file] = f.read()# add the file name and its contents to the dictionary
    return dic # return the dictionary
        


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    lst = [] # list to store the words # tokenize the document
    for word in word_tokenize(document): # iterate through the words
        if word not in string.punctuation and word.lower() not in nltk.corpus.stopwords.words("english"):
            lst.append(word.lower())
    return lst # return the list of words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dic = {} # dictionary to store the words and their idf values
    total_docs = len(documents) # total number of documents

    unique_words = set() # set to store the unique words in all the documents
    unique_words = set(word for lst in documents.values() for word in lst) # iterate through the words in all the documents and add them to the set
    for word in unique_words:
        count = 0
        for lst in documents.values():
            if word in lst:
                count += 1
        dic[word] = math.log(total_docs / count) # calculate the idf value of the word and add it to the dictionary
    return dic # return the dictionary

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    topfile  = {} #list to store the top files
    for filename , filecontent in files.items(): # iterate through the files
        score = 0# variable to store the score of the file
        for word in query:  # iterate through the words in the query
            if word in filecontent:
                score += filecontent.count(word) * idfs[word]
        if score != 0:
            topfile[filename] = score
    sortedscore = [k for k, v in sorted(topfile.items(), key=lambda x: x[1], reverse=True)]
    return sortedscore[:n]




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topsentence = {}
    for sentence , sentencecontent in sentences.items():
        score = 0
        for word in query:
            if word in sentencecontent:
                score += idfs[word]
        if score != 0:
            density = sum([sentencecontent.count(word) for word in query]) / len(sentencecontent)
            topsentence[sentence] = (score , density)
    sortedscore = [k for k, v in sorted(topsentence.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]

    return sortedscore[:n]



if __name__ == "__main__":
    main()
