import codecs
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


vectorizers = ('CountVectorizer', 'TfVectorizer', 'TfidfVectorizer', 'TweetGloVe', 'WikiGloVe')

# documents -> vectors
# return sparse.csr_matrix, string
def input_embedding(vectorizer_id, lines):
    vectorizer_string = vectorizers[vectorizer_id]
    if vectorizer_id == 0:
        embedding = CountVectorizer(strip_accents='unicode').fit_transform(lines)
    elif vectorizer_id == 1:
        embedding = TfidfVectorizer(use_idf=False).fit_transform(lines)
    elif vectorizer_id == 2:
        embedding = TfidfVectorizer(use_idf=True).fit_transform(lines)
    elif vectorizer_id == 3:
        embedding = glove_fit_transform(lines, vectorizers[vectorizer_id])
    elif vectorizer_id == 4:
        embedding = glove_fit_transform(lines, vectorizers[vectorizer_id])
    else:
        raise ValueError("Unknown vectorizer: " + str(vectorizer_id))

    print("Documents x Features = [%d x %d]" % (embedding.shape[0], embedding.shape[1]))
    return embedding, vectorizer_string


# Read input data consisting of lines with exactly 1 hashtag.
# Return lists of the extracted hashtags along with the input lines
def load_data(src_file):
    with codecs.open(src_file, mode='r', encoding='utf-8') as input_file:
        input_lines = [line.rstrip() for line in input_file.readlines()]
        hash_split = [line.split("#")[1] for line in input_lines]
        hashtags = [line.split(None)[0] for line in hash_split]
    return hashtags, input_lines

# Count occurrences of hashtags.
# Return
#       tagmap: mapping of hashtags -> number of occurences
#       taglist: list of hashtags sorted by number of occurrences
#       hashids: hashtags from input document encoded as their corresponding indices in taglist
#       cluster_cnt: number of distinct hashtags, which is 10
# Since Python 3.7*, dictionaries are order-preserving,
def mktagmap(hashtags):
    tagmap = {}
    for tag in hashtags:
        if tag in tagmap:
            tagmap[tag] = 1 + tagmap[tag]
        else:
            tagmap[tag] = 1
    taglist = sorted(tagmap, key=tagmap.get)
    cluster_cnt = len(taglist)
    hashids = [taglist.index(tag) for tag in hashtags]
    print("Hashtags [%d]:" % cluster_cnt)
    for t in range(len(taglist)):
        print("\t%2d: %s -> %d" % (t, taglist[t], tagmap[taglist[t]]))
    return tagmap, taglist, hashids, cluster_cnt

# GloVe embedding: converts tweets to vectors
# Returns sparse matrix
def glove_fit_transform(input_lines, model_name):
    model_file = "../models/%s" % model_name
    embdict = {}  # words -> vectors

    with open(model_file, 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embdict[word] = vector

    lines_words_vectors = []
    for in_line in input_lines:
        words_as_vectors = []
        for word in in_line.split(" "):
            if word[0] == '@' or word[0] == '#':
                word = word[1:]
            try:
                word_vec = embdict[word]
                words_as_vectors.append(word_vec)
            except KeyError:
                pass
        lines_words_vectors.append(words_as_vectors)

    doc_vectors = []
    for words_as_vectors, lino in zip(lines_words_vectors, range(len(lines_words_vectors))):
        lav = np.average(words_as_vectors, axis=0)
        avn = np.linalg.norm(lav)
        doc_vectors.append(lav / avn)

    embedding = sparse.csr_matrix(doc_vectors)

    return embedding


