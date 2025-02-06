import inspect
import os
import sys

import numpy as np
from sklearn.cluster import SpectralClustering, k_means
from sklearn.manifold import spectral_embedding
from sklearn.metrics.pairwise import cosine_similarity

from print_matrix import select_best_f, fb_score, print_clustering
from data import load_data, mktagmap, input_embedding

eid = int(sys.argv[1]) if len(sys.argv) > 1 else 0                                # vectorizer id = 0..4, see vectorizers in data.py
rpt = int(sys.argv[2]) if len(sys.argv) > 2 else 1                                # number of repetitions of each experiment
exp = sys.argv[3].split("-") if len(sys.argv) > 3 and sys.argv[3] != "-" else []  # experiment code d = 0..5, or list of, separated by '-', see experiments dict
lap = sys.argv[4][0] if len(sys.argv) > 4 else 'N'                                # N = normalized, C = combinatorial laplacian
ifn = sys.argv[5] if len(sys.argv) > 5 else "../Data/Data_0"                      # input data

print("Dataset: %s" % os.path.basename(ifn))

hashtags, input_lines = load_data(ifn)                      # list of hashtags and list of lines, one hashtag per line
tagmap, taglist, tagids, cluster_cnt = mktagmap(hashtags)   # mapping of hashtags to numbers of occurrences
vectors, vectrstr = input_embedding(eid, input_lines)       # embedding and its string representation


cosimat = cosine_similarity(vectors)
cosimat[cosimat > 1] = 1                     # Fix invalid (> 1) cosine values
cosimat_neg_cnt = np.sum(cosimat < 0)
deg = np.sum(cosimat, axis=1)
cosimat_neg_deg_cnt = np.sum(deg < 0)
arccosmat = np.arccos(cosimat)
np.fill_diagonal(arccosmat, 0)
cosimat_arccosmax = np.max(arccosmat)

# names -> functions to be applied on similarity matrix
experiments = {
    "zero negative":                     lambda s: 0 if s < 0 else s,
    "s + %d":                            lambda s, c: s + c,
    "(s + %d)/(1 + %d)":                 lambda s, c: (s + c)/(1 + c),
    "cos((π/2)*arccos(s)/maxarccos(S))": lambda s: np.cos((np.pi/2) * np.arccos(s) / cosimat_arccosmax),
    "cos(arccos(s)/(1+%d))":             lambda s, c: np.cos(np.arccos(s)/(1+c)),
    "exp(-(1-(s+%d))/2)":                lambda s, c: np.exp(-(1-(s+c))/2),
}

# Process similarity matrix with the supplied function
def run_exp_on_matrix(ex_name, ex_func, f_arg=None):
    matr = cosimat.copy()
    print("Processing experiment \'%s\', negative elements and rows before: (%d, %d)" % (ex_name, cosimat_neg_cnt, cosimat_neg_deg_cnt), end='')
    if f_arg is None:
        matr = np.vectorize(ex_func)(matr)
    else:
        matr = np.vectorize(ex_func)(matr, f_arg)
    np.fill_diagonal(matr, 0)
    neg_cnt = np.sum(matr < 0)
    degs = np.sum(matr, axis=1)
    neg_deg_cnt = np.sum(degs < 0)
    print(", after: (%d, %d)." % (neg_cnt, neg_deg_cnt))
    return matr

# Repeat spectral clustering rpt many times
def repeat_spectral_clustering(data, normed=True):
    reslts = []
    for r in range(rpt):
        try:
            if normed:
                sc = SpectralClustering(n_clusters=cluster_cnt, affinity='precomputed')
                cls = sc.fit_predict(data)
            else:
                maps = spectral_embedding(data, norm_laplacian=False, n_components=cluster_cnt, drop_first=False)
                _, cls, _ = k_means(maps, cluster_cnt)
            reslts.append(cls)
        except ValueError as err:
            print("Error in spectral clustering, run=%d, reason: %s" % (r, str(err)))
    if len(reslts) == 0:
        raise Exception("No results due to invalid matrix values")
    return reslts

# Print summary of the reults
def print_spectral_clustering(clus, bc, ac, wc, stdv, einfo):
    exp_info = ", \tExperiment: \'%s\', \tLaplacian: %s" % (einfo, 'Normalized' if lap == 'N' else 'Combinatorial')
    topmsg = "Affinity: precomputed, \tVectorizer: %s, \trepeat: %d%s" % (vectrstr, rpt, exp_info)
    scoreline = "best=%.6f, avg=%.6f, worst=%.6f, stdev=%.6f" % (bc, ac, wc, stdv)
    botmsg = "F-score: %.6f (%s)" % (fb_score(tagids, clus), scoreline)
    print_clustering(tagids, clus, cluster_cnt, topmsg, botmsg, taglist)


# Prepare list of experiments to process.
# The list contains pairs (name, function).
# The contents of the experiment list is determined by the argument exp which is a number o list of numbers.
exp_codes = exp if len(exp) else [str(i) for i in range(len(experiments))]
exp_names = list(experiments.keys())
exp_funcs = list(experiments.values())
exp_list = []
for exp_code in exp_codes:
    ex_id = int(exp_code)
    ex_C = 4
    exp_n = exp_names[ex_id]
    exp_f = exp_funcs[ex_id]
    fsignature = inspect.signature(exp_f)
    if len(fsignature.parameters) == 1:
        exp_list.append((exp_n, exp_f))
    elif len(fsignature.parameters) == 2:      # for two-argument functions, the second parameter is substituted by values 0..3 to produce 4 experiment items
        for c in range(ex_C):
            exp_name = exp_n % ((c,) * exp_n.count('%'))
            exp_list.append((exp_name, exp_f, c))
    else:
        raise Exception("Invalid argument count: %d" % len(fsignature.parameters))


for ex in exp_list:
    print("=" * 127)
    try:
        # modify similarity matrix with the function passed in ex tuple
        matrix = run_exp_on_matrix(*ex)
        # perform spectral clustering rpt many times, return all results
        results = repeat_spectral_clustering(matrix, normed=(lap == 'N'))
        # select the best of results, also return F-scores
        clusters, bestc, wsc, asc, stdev = select_best_f(tagids, results)
        # print summary of the results
        print_spectral_clustering(clusters, bestc, asc, wsc, stdev, ex[0])
    except Exception as exc:
        print("Spectral clustering failed: %s" % exc)

