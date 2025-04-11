
# About
Source code and experiment results for the paper
_"A method for Handling Negative Similarities in Explainable Graph Spectral Clustering of Text documents"_
by
Mieczysław A. Kłopotek,
Sławomir T. Wierzchoń,
Bartłomiej Starosta,
Dariusz Czerski, 
Piotr Borkowski.

# Operation

1. Read input data (tweets with hashtags). 
2. Embed it as vectors using one of 5 vectorization methods.
3. Compute cosine similarity matrix.
4. Transform the matrix with function (experiment).
5. Perform spectral clustering (30 times to achieve good result):
    1. Do spectral embedding with combinatorial or normalized laplacian,
    2. Execute k-means algorithm.
6. Select best result according to F measure.
7. Print summary.


# Directory structure

## `Data`
Input data: 5 sets of tweets with exactly one hashtag.
Each dataset contains 10 different hashtags.

## `Results`
The results of experiments.
Filename structure:
- `Data_n`:  input dataset
- `N` or `C`: normalised or combinatorial laplacian used
- `Exp_[0-5]|All` - experiments, i.e., functions applied to similarity matrix as listed in the `experiments` dictionary in `ICCS25_Experiments.py` 
- `Fscore` - average F measure values for experiments


## `Python`
The source code.
Start with `ICCS25_Experiments.py`.

Arguments:
1. digit `0-4`: vectorizer to use, as listed in `vectorizers` in `data.py` (default `0` = `CountVectorizer`).
2. number of repetitions of each experiment (default 1).
3. digit `0-5` or sequence of such digits, separated with `-`: experiment(s) to process as listed  in the `experiments` dictionary in `ICCS25_Experiments.py`. Single '-' denotes all experiments. Default is to do all.
4. `C` or `N`: combinatorial or normalised laplacian to use. Default is 'N'.
5. Input file name. Default is `../Data/Data_0`.

## `models`
Since GloVe model files are large (almost 1GB), instead of storing them direcly we include instructions how to download them from the source.
Two models are used: 
- `glove.twitter.27B.100d.txt` as `TweetGloVe`
- `glove.6B.100d.txt` as `WikiGloVe`.

They are available at `https://nlp.stanford.edu/projects/glove/` in `Download pre-trained word vectors` section.

# Experiments

[Click to read more about experiments and results](Experiments.md)

# Requirements

1. `Python >= 3.7` for ordering of dictionary keys.

