# Billboard Hit Prediction

Can the words of a song predict whether it reaches the Billboard Hot 100 top ten? A classification study built on lyrics alone, and an honest account of where it breaks down.

## The problem

Labels and A&R teams decide which songs get promotional money before anyone knows how they will chart. Most predictive work in this space leans on audio features such as danceability and tempo. This project asks a narrower question: with no audio information at all, how much signal is there in the lyrics themselves?

## Data

3,397 Billboard-charting songs from 2000 through 2023, covering 2,080 unique songs and 1,039 artists, with a full lyric text attached to each. The target is binary, whether the song reached the top ten, which 339 songs did, giving a 10.0 percent positive rate.

The dataset shipped with thirteen Spotify audio features attached, and 85.7 percent of those values were missing. Rather than impute five sixths of a feature block, all thirteen were dropped, which is what turned this into a lyrics-only study.

## Features

Three engineered from the lyric text. Length in words. Sentiment, scored with VADER, which is built for the informal and emphatic language lyrics tend to use. Repetitiveness, the ratio of unique words to total words, standing in for how hook-driven a song is.

The exploratory work suggested all three were worth keeping. Top ten rate peaks at 11.9 percent for songs in the second length quartile and falls to 8.3 percent for the longest, an inverted U rather than a straight line. Top ten songs also skew positive, 76.7 percent carrying positive lyrical tone against 71.9 percent of the rest, with mean sentiment of 0.533 against 0.438.

## Results

Stratified 80/20 split, 2,717 training rows and 680 test rows, class balance preserved in both.

| Metric | Logistic regression | Random forest |
|---|---|---|
| AUC-ROC (test split) | 0.542 | 0.778 |
| Accuracy | 0.46 | 0.93 |
| Precision (top ten) | 0.11 | 0.77 |
| Recall (top ten) | 0.63 | 0.49 |
| F1 (top ten) | 0.19 | 0.59 |

The random forest is clearly the better model, which makes sense given the inverted U relationship between length and success that a linear boundary cannot represent.

## The caveat that matters

Cross-validation tells a less flattering story than the single split. Mean CV AUC is 0.704 for the random forest against 0.778 on the held-out split, and 0.534 for logistic regression.

The reason is in the data. 1,848 rows carry duplicate lyric text, and 288 unique lyric texts appear on both sides of the train/test split. Some of that is cover versions and collaborations released separately, as with three different artists charting "Thank God I Found You," and some is the same song charting across multiple weeks. Either way the model sees test lyrics during training, and the single-split number is optimistic because of it.

The cross-validated 0.704 is the figure I would defend. Deduplicating by lyric text before splitting is the correct fix and is the first thing I would change.

## What it suggests

Lyrics carry real but modest signal. An AUC near 0.70 is well above chance and well below anything you would bet a marketing budget on, which is roughly the honest answer to the original question. Length and repetitiveness contribute more than sentiment does.

## Files

| File | Contents |
|---|---|
| `billboard_hit_prediction_final.ipynb` | Full analysis: EDA, NLP feature engineering, both models, cross-validation, leakage audit |
| `milestone_modeling.ipynb` | Earlier modeling milestone |
| `billboard_hit_prediction_paper.docx` | Written analysis |
| `final_writeup.docx`, `final_writeup_draft.docx` | Term paper and earlier draft |
| `project_proposal.docx` | Original proposal |
| `BBHot100.csv` | Chart data with lyrics |
| `*.png` | Confusion matrix, ROC curve, feature importance, correlation heatmap, and the EDA charts |

## Running it

```bash
pip install pandas numpy scikit-learn nltk vaderSentiment matplotlib seaborn
jupyter lab billboard_hit_prediction_final.ipynb
```

`BBHot100.csv` is included. The larger cleaned lyric corpus used during exploration is not, as it exceeds GitHub's file size limit.

## Reference

Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. *Proceedings of the International AAAI Conference on Web and Social Media, 8*(1), 216-225.
