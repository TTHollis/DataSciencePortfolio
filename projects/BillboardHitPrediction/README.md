# Billboard Hit Prediction

Can lyrics alone predict whether a song reaches the Billboard Hot 100 top ten? The first answer looked like yes. Auditing my own results showed the answer is no, and why.

## The question

Labels decide which songs get promotional money before anyone knows how they will chart. Most predictive work in this space leans on audio features such as danceability and tempo. This project asks a narrower question: with no audio information at all, how much signal is there in the words?

## Data

3,397 Billboard-charting records from 2000 through 2023, each with a full lyric text attached. The target is binary, whether the song reached the top ten.

The dataset shipped with thirteen Spotify audio features, 85.7 percent of which were missing. Rather than impute five sixths of a feature block, all thirteen were dropped, which is what made this a lyrics-only study.

Three features were engineered from the lyric text: length in words, sentiment scored with VADER, and repetitiveness measured as the share of meaningful words that appear more than once.

## The first result

A stratified 80/20 split, logistic regression and random forest, both with balanced class weights. The random forest returned an AUC-ROC of 0.778 and an F1 of 0.59 on the top-ten class. That looked like a real, if modest, finding.

Cross-validation disagreed. Five-fold stratified CV put the random forest at 0.704, well below the single-split figure. A gap that size between a hold-out score and a cross-validated one usually means the split is doing something the folds are not, so I went looking.

## What the audit found

The dataset contains 781 groups of rows sharing identical lyric text, and 288 of those texts appeared on both sides of the train/test split. The model was being tested on songs it had already memorized.

Breaking the duplicates down explains why they exist:

| Duplicate type | Groups |
|---|---|
| Spanning multiple credited artists | 600 |
| Spanning multiple chart years | 248 |
| Carrying conflicting top-ten labels | 49 |

The multi-artist case is the dominant one, and it is a mismatch between the data and the chart it describes. "Thank God I Found You" occupies three rows, one each for Mariah Carey, Joe, and 98 Degrees. Billboard counts that as a single entry. The same is true of a chart run that crosses a year boundary, and of official remixes, which Billboard pools with the original rather than charting separately unless the remix is reworked enough to count as a new song.

So the rows in this dataset are not chart entries. Treating them as though they were both leaked across the split and weighted popular collaborations several times over in training.

## The correction

Each lyric text is collapsed to one row before splitting. Where a song's rows disagreed on the label, the peak is taken, since a song that reached the top ten under any credit or in any year reached the top ten. That resolves the 49 conflicts by rule rather than by row order.

3,397 rows become 2,330. The top-ten rate is 11.0 percent.

## The corrected result

| Metric | Logistic regression | Random forest |
|---|---|---|
| AUC-ROC, hold-out split | 0.522 | 0.516 |
| AUC-ROC, 5-fold CV | 0.514 | 0.449 |
| Precision, top ten | 0.11 | 0.00 |
| Recall, top ten | 0.57 | 0.00 |

Both models are at chance. The random forest cross-validates slightly below it and predicts no top-tens at all despite balanced class weights. The 0.778 was memorization, and so, in smaller part, was the 0.704, since duplicates were spread across the cross-validation folds as well.

## Why there is no signal

Two reasons, and the second is the more interesting one.

The features are thin. Three summary statistics discard nearly everything about a lyric: its subject, its structure, its vocabulary. Exploratory analysis did show top-ten songs skewing more positive in sentiment and clustering at mid-range lengths, but a difference in group averages is not the same as a boundary that separates individual songs, and here it was not one.

More fundamentally, the dataset has no control group. Every row is a song that charted on the Hot 100. So the question the model can actually answer is not whether lyrics help a song succeed, it is whether lyrics separate the top ten from ranks eleven through one hundred among songs that already succeeded. Repetition and hooks may well drive whether a song charts at all. This data cannot test that, because the songs that never made it are absent.

## What a working version would need

A sample of songs that never charted, so the comparison has something to push against. The lyrics themselves vectorized with TF-IDF or embeddings rather than collapsed to three numbers. Artist track record, since a known act's release starts from a different place than an unknown one. Release year, since the chart's methodology and the streaming era changed what charting means partway through this window.

## Files

| File | Contents |
|---|---|
| `billboard_hit_prediction_final.ipynb` | Full analysis: EDA, NLP features, duplicate audit, deduplication, both models, cross-validation, post-fix leakage check |
| `milestone_modeling.ipynb` | Earlier modeling pass, retained as the pre-correction version |
| `billboard_hit_prediction_paper.docx` | Written analysis |
| `final_writeup.docx`, `final_writeup_draft.docx` | Term paper and earlier draft |
| `project_proposal.docx` | Original proposal |
| `BBHot100.csv` | Chart data with lyrics |
| `*.png` | Confusion matrix, ROC curve, feature importance, correlation heatmap, EDA charts |

The written documents predate the correction and report the original figures. They are kept as the record of what was submitted; this README and the final notebook carry the corrected result.

## Running it

```bash
pip install pandas numpy scikit-learn nltk vaderSentiment matplotlib seaborn
jupyter lab billboard_hit_prediction_final.ipynb
```

`BBHot100.csv` is included in this folder.

## Reference

Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. *Proceedings of the International AAAI Conference on Web and Social Media, 8*(1), 216-225.
