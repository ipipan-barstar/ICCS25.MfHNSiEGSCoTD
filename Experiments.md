
# Experiments


We have performed experiments on the effectivity of GSC methods predicting hashtags for a large body of tweets, 
using various methods of handling negativity, mentioned in the formulas (13), (14), (16), (17), (19), (7) for c = 0, 1, 2, 3. 
For the modified similarity matrices, both combinatorial and normalized Laplacians were used in GSC. 
The computations were performed for the traditional Term Vector Space (TVS, tf, tfidf) 
as well as for the GloVe based embeddings: 
TweetGlove (trained on Twitter data) and WikiGlove (trained on Wikipedia Data).
The clustering experiments were performed with popular Python libraries: numpy, scipy, scikit-learn and soyclustering 
which is an implementation of spherical k-means. 
In particular, we used SpectralClustering class from scikit-learn with two distinct settings of the affinity parameter: 
precomputed (affinity from similarity matrix) as a representative of the L-embedding and L-embedding based clustering.

## Data Set Description

For the initial experiment we used a set named en.Size=150.TagCap=300.SEL.10tags, 
consisting of random tweets published on Twitter (now X) between 2019 and 2023, 
with a length of more than 150 characters each, 
which are a collection of tweets related to the hashtags listed in Table 1.

Table 2 characterizes the dataset en.Size=150.TagCap=300.SEL.10tags 
with respect to the two GloVe-based embeddings for the five considered samples. 
Obviously, the Term Vector Space embeddings have no negative similarity problems, so they were not included. 
TweetWiki embedding leads to numerous negative similarity matrix entries, 
but no problem with row sums occurs for our samples. 
The most difficult problems occur for the WikiGloVe embedding, 
as there are many more negative similarities and there are multiple rows with negative entries in three of the samples.

## Results

Subsequent tables present clustering results for the Sample 0. 
Results for other samples can be accessed in the folder `Results`.

Let us first consider normalized Laplacians.
Table 3 presents clustering results when the correction of negative similarities is based on zeroing them.
Normalized Laplacian based clustering could be executed. 
We see that modern (GloVe based) do not have a big advantage over traditional (TVS based) embeddings. 
The results are the worst compared to other methods.

Table 4, formula (13), presents clustering results when the correction of negative similarities is based on adding a constant to all off-diagonal similarities. 
Normalized Laplacian-based clustering could be executed except for `c = 0` in WikiGlove embedding because the diagonal of D contained negative entries. 
We see that modern (GloVe based) does not have any real advantage over traditional (TVS based) embeddings. 
At the same time, we see that adding the constant `c = 1` significantly improves the performance, while higher constants do not contribute much to the results.

Table 4, formula (14) presents clustering results when the correction of negative similarities is based on adding a constant to all off-diagonal similarities and dividing for normalization. 
As expected, no improvement over Table 4 (13) is visible.

Table 5 (Normalized) presents the results when normalizing over the largest angle between document vectors. 
The results are worse for TVS embeddings, and slightly worse for GloVe embeddings.

Table 6 (formula 17) presents the results when dividing the angle between document vectors. 
The results constitute an improvement when dividing by at least two, but dividing by higher values does not contribute anything.

Table 6 (formula 19) presents the results when replacing primary similarities with their exponential variants. 
The variants do not differ much, but replacement of negative similarities with exponential ones helps the GloVe based embeddings,
and also the TVS embeddings benefit from this transformation.

As visible in the Tables 3, 5, the results for combinatorial Laplacians are significantly worse, 
and the effects of transformations are generally marginal, as expected.

Conclusions: removal of negative similarities allows to compute or improve clustering results for GloVe embeddings
whereby setting negatives to zero is the worst method. 
The transformations studied are also helpful for TVS based clustrings, whereby the reason for this effect needs to be studied deeper.

# Tables

## Table 1

TWT.10 datasets - hashtags and cardinalities of the set of related tweets used in the experiments in each sample

### Sample 0 

| No. | hashtag               | count |
|-----|-----------------------|-------|
| 0   | 90dayfiance           | 316   |
| 1   | tejran                | 345   |
| 2   | ukraine               | 352   |
| 3   | tejasswiprakash       | 372   |
| 4   | nowplaying            | 439   |
| 5   | anjisalvacion         | 732   |
| 6   | puredoctrinesofchrist | 831   |
| 7   | 1                     | 1105  |
| 8   | lolinginlove          | 1258  |
| 9   | bbnaija               | 1405  |

 ### Sample 1   

| No. | hashtag     | count |
|-----|-------------|-------|
| 0   | bb23        | 1723  |
| 1   | lfc         | 1751  |
| 2   | aewdynamite | 1821  |
| 3   | blm         | 1849  |
| 4   | trump       | 1910  |
| 5   | maga        | 2079  |
| 6   | shinycheck  | 2235  |
| 7   | nufc        | 2435  |
| 8   | cdnpoli     | 2451  |
| 9   | 2           | 2772  |

### Sample 2 

| No. | hashtag    | count |
|-----|------------|-------| 
| 0   | rhobh      | 1298  |
| 1   | robostopia | 1323  |
| 2   | gh         | 1398  |
| 3   | lufc       | 1470  |
| 4   | btc        | 1487  |
| 5   | demdebate  | 1491  |
| 6   | browns     | 1493  |
| 7   | brexit     | 1607  |
| 8   | bb22       | 1622  |
| 9   | covid\_19  | 1696  |

### Sample 3 

| No. | hashtag   | count |
|-----|-----------|-------| 
| 	 0 | s         | 1141  |
| 	 1 | sidnaaz   | 1153  |
| 	 2 | anitwt    | 1154  |
| 	 3 | breaking  | 1154  |
| 	 4 | rhop      | 1154  |
| 	 5 | treasure  | 1162  |
| 	 6 | cfc       | 1167  |
| 	 7 | trump2020 | 1222  |
| 	 8 | avfc      | 1278  |
| 	 9 | 3         | 1293  |

### Sample 4 

| No. | hashtag      | count |
|-----|--------------|-------| 
| 0   | mentalhealth | 1003  |
| 	 1 | bbcqt        | 1025  |
| 	 2 | vote         | 1025  |
| 	 3 | dnd          | 1031  |
| 	 4 | r4today      | 1036  |
| 	 5 | nffc         | 1036  |
| 	 6 | smackdown    | 1063  |
| 	 7 | debates2020  | 1065  |
| 	 8 | election2020 | 1093  |
| 	 9 | nfl          | 1122  |

## Table 2 

Properties of the dataset  en.Size=150.TagCap=300.SEL.10tags - the number of negative similarities ($S$ matrix) and the number of negative elements of the row sum matrix (`D` matrix) 
in each sample. 

| Sample | Embedding type | negative `S` entries | negative `D` entries |
|--------|----------------|----------------------|----------------------| 
| 0      | WikiGloVe      | 4256724              | 171                  |
| 0      | TweetGloVe     | 242824               | 0                    |
| 1      | WikiGloVe      | 147268               | 3                    |
| 1      | TweetGloVe     | 14                   | 0                    |
| 2      | WikiGloVe      | 2032                 | 0                    |
| 2      | TweetGloVe     | 0                    | 0                    |
  

| Sample | Embedding type | negative `S` entries | negative `D` entries |
|--------|----------------|----------------------|----------------------| 
| 3      | WikiGloVe      | 54                   | 0                    |
| 3      | TweetGloVe     | 16                   | 0                    | 
| 4      | WikiGloVe      | 52552                | 2                    |
| 4      | TweetGloVe     | 0                    | 0                    |
  
## Table 3

Clustering results for the dataset en.Size=150.TagCap=300.SEL.10tags Sample 0 after similarity correction (setting negative `s_{ik}` to zero)  - F-score, averaged over 30 runs when Normalized  and Combinatorial Laplacian based GSC was applied.

### Normalized Laplacian

| Embedding type  | avg. F-score | SD of  F-score | 
|-----------------|--------------|----------------|
| CountVectorizer | 0.048        | 0.035          | 
| TfVectorizer    | 0.037        | 0.019          | 
| TfidfVectorizer | 0.025        | 0.007          | 
| WikiGloVe       | 0.045        | 0.022          | 
| TweetGloVe      | 0.060        | 0.036          | 


### Combinatorial Laplacian 

| Embedding type  | avg. F-score | SD of  F-score | 
|-----------------|--------------|----------------|
| CountVectorizer | 0.0189       | 0.000          | 
| TfVectorizer    | 0.019        | 0.000          | 
| TfidfVectorizer | 0.022        | 0.001          | 
| WikiGloVe       | 0.020        | 0.001          | 
| TweetGloVe      | 0.018        | 0.000          | 


## Table 4


### Using formula (13)


Clustering results of the dataset en.Size=150.TagCap=300.SEL.10tags Sample 0 
after similarity correction using formula (13) (adding $c$ to all off-diagonal similarities). 
F-score, averaged over 30 runs when normalized Laplacian based GSC was applied.
Rows marked with `N/A' refer to executions failed  due to negative values of similarities.

| Embedding type  | `c` | avg. F-score | SD of  F-score | 
|-----------------|-----|--------------|----------------| 
||||                | 
| CountVectorizer | 0   | 0.039        | 0.022          | 
| CountVectorizer | 1   | 0.083        | 0.029          | 
| CountVectorizer | 2   | 0.095        | 0.044          | 
| CountVectorizer | 3   | 0.091        | 0.042          | 
||||                | 
| TfVectorizer    | 0   | 0.038        | 0.026          | 
| TfVectorizer    | 1   | 0.092        | 0.052          | 
| TfVectorizer    | 2   | 0.093        | 0.041          | 
| TfVectorizer    | 3   | 0.093        | 0.034          | 
||||                | 
| TfidfVectorizer | 0   | 0.026        | 0.009          | 
| TfidfVectorizer | 1   | 0.089        | 0.058          | 
| TfidfVectorizer | 2   | 0.087        | 0.054          | 
| TfidfVectorizer | 3   | 0.101        | 0.057          | 
||||                | 
| WikiGloVe       | 0   | N/A          | N/A            | 
| WikiGloVe       | 1   | 0.070        | 0.026          | 
| WikiGloVe       | 2   | 0.093        | 0.050          | 
| WikiGloVe       | 3   | 0.088        | 0.051          | 
||||                | 
| TweetGloVe      | 0   | 0.064        | 0.036          | 
| TweetGloVe      | 1   | 0.081        | 0.047          | 
| TweetGloVe      | 2   | 0.099        | 0.059          | 
| TweetGloVe      | 3   | 0.084        | 0.060          | 
  


### Using formula (14)

Clustering results of the dataset en.Size=150.TagCap=300.SEL.10tags, Sample 0 after similarity correction
using formula (14) (adding `c` and dividing by `1+c` to all off-diagonal similarities). 
F-score, averaged over 30 runs when normalized Laplacian based GSC was applied.  
Rows marked with `N/A' refer to executions failed  due to negative values of similarities.

| Embedding type  | `c` | avg. F-score | SD of  F-score | 
|-----------------|-----|--------------|----------------| 
||||| 
| CountVectorizer | 0   | 0.039        | 0.022          | 
| CountVectorizer | 1   | 0.090        | 0.036          | 
| CountVectorizer | 2   | 0.091        | 0.044          | 
| CountVectorizer | 3   | 0.098        | 0.038          | 
||||| 
| TfVectorizer    | 0   | 0.038        | 0.026          | 
| TfVectorizer    | 1   | 0.088        | 0.040          | 
| TfVectorizer    | 2   | 0.080        | 0.028          | 
| TfVectorizer    | 3   | 0.088        | 0.044          | 
||||| 
| TfidfVectorizer | 0   | 0.026        | 0.009          | 
| TfidfVectorizer | 1   | 0.082        | 0.042          | 
| TfidfVectorizer | 2   | 0.086        | 0.058          | 
| TfidfVectorizer | 3   | 0.096        | 0.055          | 
||||| 
| WikiGloVe       | 0   | N/A          | N/A            | 
| WikiGloVe       | 1   | 0.094        | 0.039          | 
| WikiGloVe       | 2   | 0.079        | 0.044          | 
| WikiGloVe       | 3   | 0.084        | 0.051          | 
||||| 
| TweetGloVe      | 0   | 0.064        | 0.036          | 
| TweetGloVe      | 1   | 0.083        | 0.060          | 
| TweetGloVe      | 2   | 0.085        | 0.064          | 
| TweetGloVe      | 3   | 0.088        | 0.058          | 

## Table 5


Clustering results of the dataset en.Size=150.TagCap=300.SEL.10tags, Sample 0 
after similarity correction using formula (16)  (transformation `s_{ik} = cos((π/2)\arccos(s_{ik}) / max arccos(s_{ik})))`).
F-score, averaged over 30 runs was applied.

### Normalized Laplacian 

| Embedding type  | avg. F-score | SD of  F-score | 
|-----------------|--------------|----------------| 
| CountVectorizer | 0.041        | 0.022          | 
| TfVectorizer    | 0.040        | 0.021          | 
| TfidfVectorizer | 0.024        | 0.007          | 
| WikiGloVe       | 0.086        | 0.038          | 
| TweetGloVe      | 0.070        | 0.041          | 
  
### Combinatorial Laplacian 

| Embedding type  | avg. F-score | SD of  F-score | 
|-----------------|--------------|----------------| 
| CountVectorizer | 0.019        | 0.000          | 
| TfVectorizer    | 0.019        | 0.000          | 
| TfidfVectorizer | 0.022        | 0.001          | 
| WikiGloVe       | 0.019        | 0.000          | 
| TweetGloVe      | 0.018        | 0.000          | 
  
## Table 6

### Using formula (17)
 Clustering results of the dataset en.Size=150.TagCap=300.SEL.10tags, 
 Sample 0 after similarity correction using formula (17) 
 (transformation `s_{ik} = cos(arccos s_{ik}/(1+c))`).
 F-score, averaged over 30 runs.
Rows marked with `N/A' refer to executions failed  due to negative values of similarities.

 
| Embedding type  | `c` | avg. F-score | SD of  F-score | 
|-----------------|-----|--------------|----------------| 
|                 |     |              |                | 
| CountVectorizer | 0   | 0.036        | 0.020          | 
| CountVectorizer | 1   | 0.092        | 0.043          | 
| CountVectorizer | 2   | 0.088        | 0.028          | 
| CountVectorizer | 3   | 0.093        | 0.040          | 
|                 |     |              |                |
| TfVectorizer    | 0   | 0.035        | 0.017          | 
| TfVectorizer    | 1   | 0.077        | 0.043          | 
| TfVectorizer    | 2   | 0.096        | 0.039          | 
| TfVectorizer    | 3   | 0.088        | 0.044          | 
|                 |     |              |                |
| TfidfVectorizer | 0   | 0.025        | 0.001          | 
| TfidfVectorizer | 1   | 0.081        | 0.034          | 
| TfidfVectorizer | 2   | 0.073        | 0.036          | 
| TfidfVectorizer | 3   | 0.087        | 0.058          | 
|                 |     |              |                |
| WikiGloVe       | 0   | N/A          | N/A            | 
| WikiGloVe       | 1   | 0.068        | 0.037          | 
| WikiGloVe       | 2   | 0.085        | 0.048          | 
| WikiGloVe       | 3   | 0.075        | 0.044          | 
|                 |     |              |                |
| TweetGloVe      | 0   | 0.081        | 0.044          | 
| TweetGloVe      | 1   | 0.081        | 0.066          | 
| TweetGloVe      | 2   | 0.081        | 0.054          | 
| TweetGloVe      | 3   | 0.084        | 0.043          | 
  


### Using formula (19)

Clustering results of the dataset en.Size=150.TagCap=300.SEL.10tags, Sample 0 
after similarity correction using formula (19)
(transformation `s_{ik} = exp(-(1-(s_{ik}+c))/2)`).
F-score, averaged over 30 runs when normalized Laplacian based GSC was applied.

| Embedding type  | `c` | avg. F-score | SD of  F-score | 
|-----------------|-----|--------------|----------------| 
|                 |     |              |                | 
| CountVectorizer | 0   | 0.089        | 0.045          | 
| CountVectorizer | 1   | 0.084        | 0.036          | 
| CountVectorizer | 2   | 0.102        | 0.045          | 
| CountVectorizer | 3   | 0.080        | 0.035          | 
|                 |     |              |                |
| TfVectorizer    | 0   | 0.085        | 0.031          | 
| TfVectorizer    | 1   | 0.084        | 0.037          | 
| TfVectorizer    | 2   | 0.086        | 0.037          | 
| TfVectorizer    | 3   | 0.109        | 0.048          | 
|                 |     |              |                |
| TfidfVectorizer | 0   | 0.090        | 0.046          | 
| TfidfVectorizer | 1   | 0.088        | 0.056          | 
| TfidfVectorizer | 2   | 0.082        | 0.038          | 
| TfidfVectorizer | 3   | 0.100        | 0.065          | 
|                 |     |              |                |
| WikiGloVe       | 0   | 0.082        | 0.047          | 
| WikiGloVe       | 1   | 0.093        | 0.053          | 
| WikiGloVe       | 2   | 0.077        | 0.044          | 
| WikiGloVe       | 3   | 0.079        | 0.046          | 
|                 |     |              |                |
| TweetGloVe      | 0   | 0.074        | 0.049          | 
| TweetGloVe      | 1   | 0.085        | 0.047          | 
| TweetGloVe      | 2   | 0.088        | 0.047          | 
| TweetGloVe      | 3   | 0.080        | 0.050          | 
  
