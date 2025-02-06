import statistics
import numpy as np
import sklearn.metrics as sm

# calculate F score
def fb_score(lab_true, lab_pred):
    scr = sm.fbeta_score(lab_true, lab_pred, average='macro', beta=2)
    return scr

# Select the best result by F score.
# Also return the average, the worst and standard deviation of F score.
def select_best_f(lab_true, lab_pred_list):
    best = -1.0
    worst = 1.0
    avg = 0.0
    all_scores = []
    best_cl = None
    for cl in lab_pred_list:
        score = fb_score(lab_true, cl)
        if score > best:
            best = score
            best_cl = cl
        if score < worst:
            worst = score
        avg += score
        all_scores.append(score)
    mean = avg / len(lab_pred_list)
    stdev = statistics.stdev(all_scores, mean) if len(all_scores) > 1 else 0.0
    return best_cl, best, worst, mean, stdev

# calculate error matrix
def calc_err_matrix(lab_true, lab_pred, cluster_cnt):
    if len(lab_pred) != len(lab_true):
        print("Error: %d != %d" % (len(lab_pred), len(lab_true)))
        return -1
    err_mat = np.zeros(shape=(cluster_cnt, cluster_cnt), dtype=int)
    for x in range(len(lab_pred)):
        err_mat[lab_true[x]][lab_pred[x]] += 1
    return err_mat

# rearrange matrix columns to more or less triangle form (preseriving row order) so that it is easier to read
def rearrange_err_matr(er_mat, cluster_cnt):
    labels = list(range(cluster_cnt))
    eT = er_mat.T
    for col in range(cluster_cnt):
        max_row = col
        for row in range(col, cluster_cnt):
            if eT[row, col] > eT[max_row, col]:
                max_row = row
        if max_row != col:
            eT[[col, max_row]] = eT[[max_row, col]]
            labels[col], labels[max_row] = labels[max_row], labels[col]
    return eT.T, labels

# print coincidence matrix with auxiliary information (header, row names, etc)
def prt_err_matr(er_mat, column_labels, grp_cnt, taglist=None, max_tag_width=1):
    tagspace = " " * max_tag_width
    sch = "-"
    vert = "|"
    row_labels = [sl for sl in range(grp_cnt)]
    print("%sT\P | %s %14s<- predicted labels" % (tagspace, " ".join("%5d" % (column_labels[x]) for x in range(grp_cnt)), " "))
    line = tagspace + sch * ((1 + grp_cnt) * 6 + 5 + 2)  # 102
    print(line, end=' ')
    row_n = 0
    row_total = 0
    col_sum = [0 for x in range(len(er_mat))]
    for row in er_mat:
        if taglist:
            fmt = "\n%%%ds:%%3d%%s" % max_tag_width
            print(fmt % (taglist[row_labels[row_n]], row_labels[row_n], vert), end=' ')
        else:
            print("\n  %3d%s" % (row_labels[row_n], vert), end=' ')
        col_ind = 0
        row_sum = 0
        for cel in row:
            col_sum[col_ind] += cel
            col_ind += 1
            row_sum += cel
            print("%5d" % cel, end=' ')
        print("%s%5d" % (vert, row_sum), end=' ')
        row_n += 1
        row_total += row_sum
    col_total = sum(col_sum)
    col_summary = "    %s%s%s %s%5d\\%-5d%2s<- predicted groups %s predicted sum \\ original sum" % (tagspace, vert, "".join(" %5d" % x for x in col_sum), vert, col_total, row_total, " ", vert)
    print("\n" + line)
    print(col_summary)

# print error matrix together with any additional information passed as arguments
def print_clustering(lab_true, lab_pred, cluster_cnt, topmsg="", botmsg="", taglist=None):
    sep = "-" * 66
    max_tag_width = (1 + len(max(taglist, key=len))) if taglist else 1
    line = "-" * ((1 + cluster_cnt) * 6 + 5 + 2 + max_tag_width)
    print(sep)
    print(topmsg)
    print(line)
    err_matrix = calc_err_matrix(lab_true, lab_pred, cluster_cnt)
    rearr_error_matrix, rearr_clabels = rearrange_err_matr(err_matrix, cluster_cnt)
    prt_err_matr(rearr_error_matrix, rearr_clabels, cluster_cnt, taglist, max_tag_width)
    print(line)
    print(botmsg)
    print(sep)
