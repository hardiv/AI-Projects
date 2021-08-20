import os
import string

import nltk
import sys
from math import log
# nltk.download('stopwords')

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


def get_contents(file):
    with open(file, "r", encoding='UTF-8') as f:
        contents = f.read()
    return contents


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    dir_path = str(directory)
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        file_name = file[:-4]
        contents = get_contents(file_path)
        files[file_name] = contents
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    tokens = nltk.word_tokenize(document)
    processed = []
    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = list(string.punctuation)
    for token in tokens:
        if token not in stopwords and token not in punctuation:
            processed.append(token)
    return processed


def get_docs_containing_words(documents):
    num_docs_containing = {}
    for document in documents.keys():
        for word in set(documents[document]):
            if word in num_docs_containing.keys():
                num_docs_containing[word] += 1
            else:
                num_docs_containing[word] = 1
    return num_docs_containing


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_docs = len(documents)
    num_docs_containing = get_docs_containing_words(documents)
    idfs = {}
    for word, value in num_docs_containing.items():
        idfs[word] = log(num_docs/value)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}

    for file in files:
        tf_idfs[file] = 0
        tokens = len(files[file])
        for word in query:
            freq = 1
            if word in files[file]:
                freq = files[file].count(word) + 1
            tf = freq / tokens
            idf = 1
            if word in idfs.keys():
                idf = idfs[word]
            tf_idfs[file] += tf * idf

    sorted_files = sorted(tf_idfs, key=tf_idfs.get, reverse=True)
    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    stats = {}  # will be a dictionary of dictionaries

    for sentence in sentences:
        stats[sentence] = {}
        stats[sentence]['idf'] = 0
        stats[sentence]['word_count'] = 0
        for word in query:
            if word in sentences[sentence]:
                stats[sentence]['idf'] += idfs[word]
                stats[sentence]['word_count'] += 1
        stats[sentence]['QTD'] = float(stats[sentence]['word_count'] / len(sentences[sentence]))
    sorted_sequences = sorted(stats.keys(), key=lambda sentence: (stats[sentence]['idf'], stats[sentence]['QTD']), reverse=True)
    return sorted_sequences[:n]


if __name__ == "__main__":
    main()
