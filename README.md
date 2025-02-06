
# About
Source code and experiment results for the paper
_"A method for Handling Negative Similarities in Explainable Graph Spectral Clustering of Text documents"_
by
Mieczysław A. Kłopotek,
Sławomir T. Wierzchoń,
Bartłomiej Starosta,
Dariusz Czerski, 
Piotr Borkowski.

# Directory structure

## `Data`
Input data: 4 sets of tweets with exactly one hashtag.
Each dataset contains 10 different hashtags.

## `Results`
The results of experiments.
Filename structure:
- `Data_n`:  input data
- `N` or `C`: normalised or combinatorial laplacian used
- `Exp_[0-5]|All` - experiments, i.e., functions applied to similarity matrix as listed in the `experiments` dictionary in `ICCS25_Experiments.py` 
- `Fscore` - average Fscore values for experiments


## `Python`
The source code.
Start with `ICCS25_Experiments.py`.
Arguments:
1. digit `0-4`: vectorizer to use, as listed in `vectorizers` in `data.py` (default `0` = `CountVectorizer`).
2. number of repetitions of each experiment (default 1).
3. digit `0-5` or sequence of such digits, separated with `-`: experiment(s) to process as listed  in the `experiments` dictionary in `ICCS25_Experiments.py`. Single '-' denotes all experiments. Default it to do all.
4. `C` or `N`: combinatorial or normalised laplacian to use. Default is 'N'.
5. Filename. Default is `../Data/Data_0`.

## `models`
Since GloVe model files are large (almost 1GB), instead of storing them direcly we include instructions how to download them from the source.
Two models are used: 
- `glove.twitter.27B.100d.txt` as `TweetGloVe`
- `glove.6B.100d.txt` as `WikiGloVe`.

They are available at `https://nlp.stanford.edu/projects/glove/` in `Download pre-trained word vectors` section.



# Requirements

1. `Python >= 3.7` for ordering of dictionary keys.

[//]: # (2. ``scikit-learn <= 0.24.2``)

