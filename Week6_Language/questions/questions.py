import nltk
import sys
import os
from nltk.tokenize import word_tokenize
import string
import math
from collections import Counter

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
    
    # get the path of the current working directory
    current_dir = os.getcwd()

    # get the path to the files directory
    files_path = os.path.join(current_dir, directory)
    
    # add an entry in the files dict for each file
    # from our directory
    files = dict()

    # get the list of file names inside the directory
    files_list = os.listdir(files_path)

    # for each file name(key), add its content as value
    for file in files_list:
        with open(os.path.join(files_path, file)) as f:
            files[file] = f.read()
    
    return files



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    # split the document into tokens 
    tokens = word_tokenize(document)

    # get a list of punctuation signs 
    punctuation = string.punctuation

    # get a list of stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    # build a list with filtered words from the document
    words = []

    for word in tokens:
        if word.isalpha():
            if not word.lower() in punctuation and not word.lower() in stopwords:
                words.append(word.lower())
    
    return words



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    word_idfs = dict()

    # if the IDF value is not already computed
    # compute IDF value for each word from each document
    for document in documents:
        for word in documents[document]:
            if not word in word_idfs:
                frequency = count_word_in_documents(documents, word)
                word_idfs[word] = math.log(len(documents) / frequency)
    
    return word_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    # gather ranks for all files
    ranks = []

    # return top n files sorted by rank
    rank_files = []

    # compute rank for each file
    for file in files:
        rank  = 0

        # for each word in the query
        for word in query:

            # check if the word appears in the file
            if word in files[file]:
                # if it does appear, add the word's computed tf-idf to the 
                # rank of the file
                rank += count_word_in_document(files[file], word) * idfs[word]
        
        # save the computed rank for the file
        ranks.append((file, rank))
    
    # sort the list of files based on their ranks
    ranks.sort(key=lambda t: t[1], reverse=True)

    # return only the top n filenames
    for rank in ranks[:n]:
        rank_files.append(rank[0])

    return rank_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
   
    # gather ranks for all sentences
    ranks = []

    # return top n sentences sorted by rank
    rank_sentences = []

    # compute rank for each sentence
    for sentence in sentences:
        rank  = 0
        query_words = 0
        # for each word in the query
        for word in query:

            # check if the word appears in the sentence
            if word in sentences[sentence]:
                # if it does appear, add the word's computed idf to the 
                # rank of the sentence
                rank += idfs[word]

                # increase the number of query words that appear in the sentence
                query_words +=1
        
        # save the computed rank and query term density for the sentence
        ranks.append((sentence, rank, query_words/len(sentences[sentence])))
    
    # sort the list of sentences based on their ranks and query term density
    ranks.sort(key=lambda t: (t[1], t[2]), reverse=True)

    # return only the top n sentences
    for rank in ranks[:n]:
        rank_sentences.append(rank[0])

    return rank_sentences


def count_word_in_documents(documents, word):
    """
    Given a word and a dictionary of `documents` that maps names of documents to a list
    of words, return the number of documents in which the word appears.
    """
    count = 0

    # count the number of documents in which the word appears
    for document in documents:
        if word in documents[document]:
           count += 1

    return count


def count_word_in_document(document, word):
    """
    Given a word and a document, return how many times the word appears 
    inside the document.
    """

    doc_words = Counter(document)

    return doc_words[word]



if __name__ == "__main__":
    main()
