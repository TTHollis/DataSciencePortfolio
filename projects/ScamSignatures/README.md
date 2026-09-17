# Scam Signatures

Fraud detectors tell a job seeker that a posting is suspicious. They do not tell them why. This project drops the label and asks whether fraudulent postings organize themselves into a small number of recognizable families based on their language alone.

## The question

I have built a classifier and a fine-tuned language model on this dataset in earlier courses. Both answer one question, is this posting fraudulent, and a verdict without an explanation is hard for a job seeker to act on and hard for a trust and safety team to audit.

So this is unsupervised. Postings are clustered with the fraud label withheld, and the label is only revealed afterward to score what the clustering found. Three questions: does fraud concentrate or scatter, how many distinct signatures exist and what defines each, and do postings written in 2025 and 2026 fall into those signatures or form new ones. The first two are answered here. The third needs a corpus that does not exist yet and is the remaining work.

## Data

The Employment Scam Aegean Dataset, 17,880 real postings collected through a recruiting platform between 2012 and 2014 and annotated by that platform's own specialists. 866 are fraudulent, 4.84 percent.

Preparation is five steps. The five free text fields are joined into one document per posting and residual HTML is stripped. The dataset replaces URLs, emails, and phone numbers with placeholder tokens, so those are counted as a structural feature before being normalized to plain words, since a direct contact instruction is informative while a random hash is noise. Field presence flags are recorded before any missing value is filled, because a missing company profile is a signal rather than a defect. Then one posting with no description, one document under five words, and 2,006 exact duplicates are removed, leaving 15,872 postings at a 4.48 percent fraud rate.

Deduplication matters more than it sounds. Duplicates ran at 22.3 percent among fraudulent postings against 15.0 percent among legitimate ones, so leaving them in would have let density-based clustering find copies rather than patterns.

## Approach

Postings are embedded with all-MiniLM-L6-v2. The model truncates at 256 tokens and the median posting is longer than that, so each document is split into 180 word chunks, embedded separately, and mean pooled back to one vector. 15,872 postings become 42,327 chunks.

UMAP runs twice on cosine distance, once to five components with `min_dist=0` for clustering and once to two components with `min_dist=0.1` for the picture. HDBSCAN clusters the five dimensional space with a minimum cluster size of 25, chosen on internal evidence before labels were revealed: a sweep showed silhouette holding steady through 40 and then falling, with the largest cluster jumping from 335 to 750 members over the same interval.

TF-IDF with truncated SVD runs the same pipeline as a second representation, and K-means runs on both reduced spaces as a baseline. Everything is scored on one yardstick, which I call concentration: the share of all fraud captured by clusters running at three times base rate, divided by the share of the corpus those clusters occupy. It rewards methods that leave points unassigned and penalizes methods that do not, and it matches the question a human reviewer actually faces, which is how much reading a given amount of fraud costs.

## What it found

Fraud concentrates, but only partly. Fifteen of 173 clusters run at three times base rate or higher, holding 42.5 percent of all fraud inside 5.7 percent of the corpus. The two densest are 96.8 and 90.0 percent fraudulent. The more telling number is the noise group: postings HDBSCAN declined to cluster carried 4.01 percent fraud, below the corpus rate, which is direct evidence that fraud prefers dense, template shaped regions. The qualification is that 57 percent of fraudulent postings were not in a high lift cluster at all.

The baseline comparison reversed my starting assumption.

| Method | Fraud captured | Corpus occupied | Unassigned | Concentration |
|---|---|---|---|---|
| HDBSCAN on embeddings | 42.5% | 5.7% | 31.4% | 7.4 |
| K-means (k = 173) on embeddings | 55.8% | 8.2% | 0.0% | 6.8 |
| HDBSCAN on TF-IDF | 61.0% | 6.6% | 27.3% | 9.3 |
| K-means (k = 173) on TF-IDF | 67.7% | 9.7% | 0.0% | 7.0 |

TF-IDF beat sentence embeddings on both recall and precision. My proposal assumed semantic similarity would win because scam postings paraphrase a shared pitch. They do not paraphrase. They copy and paste, and an uncased 384 dimensional representation actively discards the brand names, dollar figures, and misspellings that identify a template.

The two representations turned out to be complementary rather than redundant. Of 711 fraudulent postings, 226 were caught by both, 76 by embeddings only, 208 by TF-IDF only, and 201 by neither. Their union captures 71.7 percent of all fraud within 9.8 percent of the corpus. That union is less efficient than TF-IDF alone, at 7.3 against 9.3, but the material it adds still concentrates at 3.3 times random, so it is worth the extra reading.

## The four archetypes

Reading the dense fraud clusters produced four recognizable shapes, together 504 postings, 3.2 percent of the corpus, carrying 47.5 percent of all fraud.

| Archetype | Postings | Fraud rate | Company profile | Logo | Screening questions | Median words |
|---|---|---|---|---|---|---|
| The Bait Ad | 71 | 92.9% | 0.0% | 4.2% | 5.6% | 81 |
| The Ghost Agency | 99 | 100% | 100% | 100% | 89.9% | 571 |
| The Borrowed Brand | 51 | 100% | 58.8% | 58.8% | 0.0% | 514 |
| The Common Form | 283 | 43.1% | 36.8% | 40.6% | 40.3% | 208 |
| Corpus baseline | 15,872 | 4.5% | 80.7% | 80.0% | 49.1% | 366 |

The Bait Ad is recognizable entirely by absence and a simple structural filter catches it reliably. The Ghost Agency is the finding that matters: a single operator advertised 60 distinct professional roles across 22 locations under at least two brand names, every posting opening with the same signature paragraph. 99 postings, all fraudulent, 13.9 percent of all fraud in the dataset. No two documents are identical, so duplicate detection misses it, but the opening paragraph is reused verbatim and shared misspellings confirm one author. Structurally those postings are flawless, carrying a company profile and logo on 100 percent of listings and screening questions on 89.9 percent, better presented than the average legitimate posting. Every absence based heuristic fails on them completely.

That is the reversal worth taking away. The crudest fraud is the easiest to catch and the most professional is the hardest, and structural completeness that reads as legitimacy is precisely what the largest operator here invested in.

## Validation

Across UMAP seeds of 42, 7, and 2026 the pipeline produced 173, 172, and 190 clusters at 31.4, 29.1, and 31.0 percent noise. Pairwise agreement on the roughly 9,800 postings clustered in every run gave adjusted Rand indices of 0.898 to 0.937 and normalized mutual information above 0.97. The structure is in the data rather than in any single initialization, though about a thousand boundary postings move between clustered and noise depending on the seed.

The silhouette based selection of k that my proposal specified does not select on this data. Silhouette rose monotonically from 0.324 at k = 10 to 0.502 at k = 173 with no elbow, because the data is one large mass plus many small satellites, so every additional centroid finds another satellite.

## Limitations

The most serious one concerns the labels. Within a single recruiter's postings there are byte identical company descriptions where the dataset labels one posting fraudulent and two others legitimate. If the label distinguishes documents that are textually indistinguishable, it encodes information outside the text, most plausibly complaints received or account action taken after publication. No text based method can recover that, and it places a ceiling on what any result here can claim.

The data is also eleven to fourteen years old, and the platform's annotations are treated as ground truth without independent verification. The archetypes are named from reading cluster members, which is interpretation rather than measurement, and a different reader might draw the lines differently.

Identifiable company and individual names surfaced by the clustering are masked in all notebook output. The source data is already public, so this is display-layer redaction rather than protection, but it keeps the analysis from republishing named accusations. The current implementation uses a hand-curated list, which does not generalize; named entity recognition is the correct fix and is on the list.

## Files

| File | Contents |
|---|---|
| `scam_signatures.ipynb` | Full analysis: preparation, chunked embedding, both clustering pipelines, baselines, validation, archetype interpretation, all five figures |
| `fig1_embedding_space.png` | Postings in two dimensional embedding space, labels withheld |
| `fig2_fraud_rate_by_cluster.png` | Fraud rate by cluster against the corpus base rate |
| `fig3_capture_vs_review.png` | Fraud captured by each representation against the share of corpus reviewed |
| `fig4_archetype_fingerprint.png` | Structural fingerprint of each archetype against the corpus baseline |
| `fig5_ghost_agency_campaign.png` | The Ghost Agency campaign across the embedding space and its job titles |
| `HollisT_Proj1MS1_DSC680.docx`, `.pdf`, `HollisT_Milestone1.odt` | Proposal and data selection |
| `HollisT_Proj1MS2_DSC680.docx` | Draft white paper |

The source dataset is not redistributed. Download `fake_job_postings.csv` from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction) into this folder to run the notebook.

## Running it

```bash
pip install pandas numpy scikit-learn sentence-transformers umap-learn hdbscan matplotlib
jupyter lab scam_signatures.ipynb
```

The notebook runs top to bottom and reproduces every figure and table above. Embeddings are cached after the first pass and all random seeds are fixed. Chunked embedding of 42,327 chunks takes a few minutes on a GPU and considerably longer on CPU.

## Status

This is an active capstone project. The first two research questions are answered; the third, whether postings written in 2025 and 2026 fall into these signatures or form new ones, requires a contemporary evaluation set that has not been assembled yet. Topic modeling within the fraud dense clusters and the switch from a curated redaction list to named entity recognition are also outstanding.

## References

Bansal, S. (2020). *Real or fake: Fake job posting prediction* [Data set]. Kaggle. https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction

Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. *arXiv*. https://doi.org/10.48550/arXiv.2203.05794

Hubert, L., & Arabie, P. (1985). Comparing partitions. *Journal of Classification, 2*(1), 193-218. https://doi.org/10.1007/BF01908075

McInnes, L., Healy, J., & Astels, S. (2017). hdbscan: Hierarchical density based clustering. *Journal of Open Source Software, 2*(11), 205. https://doi.org/10.21105/joss.00205

McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform manifold approximation and projection for dimension reduction. *arXiv*. https://doi.org/10.48550/arXiv.1802.03426

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing* (pp. 3982-3992). Association for Computational Linguistics. https://doi.org/10.18653/v1/D19-1410

Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics, 20*, 53-65. https://doi.org/10.1016/0377-0427(87)90125-7

Vidros, S., Kolias, C., Kambourakis, G., & Akoglu, L. (2017). Automatic detection of online recruitment frauds: Characteristics, methods, and a public dataset. *Future Internet, 9*(1), 6. https://doi.org/10.3390/fi9010006
