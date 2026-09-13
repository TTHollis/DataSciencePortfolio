# Job Posting Fraud Classifier

Predicting fraudulent job postings from listing text and structure, tuned so that the model misses as few scams as possible.

## The problem

Fraudulent job postings are cheap to create and expensive to fall for. A scam listing can harvest a Social Security number, collect an "equipment fee," or use a fake offer letter to open accounts in someone else's name. Job boards carry millions of listings and cannot review them by hand, so the screening has to be automated.

This project came out of my own job search. After losing a fifteen year job during COVID, I spent months reading postings, and a surprising number of them were too good to be true. The question I wanted to answer was whether the tells I was noticing by eye, vague company descriptions, missing logos, promises of high pay for entry level work, were consistent enough for a model to learn.

## Data

The Employment Scam Aegean Dataset (EMSCAD), 17,880 real job postings with 866 labeled fraudulent, a 4.84 percent fraud rate. Each posting carries free text fields (title, company profile, description, requirements, benefits), categorical fields (employment type, required experience and education, industry, function, location), and binary flags (telecommuting, has company logo, has questions).

The class imbalance and the missing data are both part of the problem rather than defects in it. Salary range is missing from 15,012 postings and department from 11,547, and whether a field is missing at all turns out to carry signal.

## Approach

Text and structure are modeled together. The free text fields are concatenated and vectorized with TF-IDF at 5,000 features, categorical fields are one-hot encoded into 2,948 columns, and engineered flags are added for whether a company profile and salary range are present along with a description length measure. The final matrix is 7,954 features wide.

The split is stratified at 80/20, giving 14,304 training rows and 3,576 test rows with the fraud rate preserved in both. SMOTE is applied to the training set only, after the split and after vectorization, so that no synthetic minority examples leak into evaluation. Two models are compared: logistic regression as an interpretable baseline and random forest as the nonlinear alternative.

Because a missed scam costs a job seeker far more than a false alarm costs a reviewer, the decision threshold is tuned for recall rather than left at the default 0.5.

## Results

Evaluated on the held-out test set of 3,576 postings, 173 of them fraudulent.

| Metric | Logistic regression (0.50) | Logistic regression (0.54) | Random forest |
|---|---|---|---|
| F1 | 0.789 | 0.812 | 0.786 |
| Precision (fraud) | 0.70 | 0.74 | 1.00 |
| Recall (fraud) | 0.91 | 0.90 | 0.65 |
| AUC-ROC | 0.989 | n/a | 0.993 |
| AUC-PR | 0.916 | n/a | 0.928 |
| Fraud caught | 157 | 156 | 112 |
| Fraud missed | 16 | 17 | 61 |
| Legitimate flagged | 68 | 55 | 0 |

The random forest has the better ranking metrics and perfect precision, and it is still the wrong model for this problem. It missed 61 of 173 scams. The tuned logistic regression misses 17 and pays for that with 55 false alarms out of 3,403 legitimate postings, which is a review queue a human can clear in an afternoon. The recommended model is logistic regression at a 0.54 threshold.

Feature importance backs up what the eye was catching: `has_company_logo` and `has_profile` are the two strongest individual features, and terms like "data entry," "earn," "work home," and "position" carry weight. Text accounts for 87.3 percent of total importance, engineered flags for 8.0 percent, and categorical fields for 4.6 percent.

## Limitations

EMSCAD was collected between 2012 and 2014, and scam language has moved on since then. Modern variants such as the paid coaching call and the fake recruiter reaching out over text are not represented in the training data at all, which is a real ceiling on how far this model generalizes. That gap is what motivated the follow-up work.

The model also predicts a label without explaining it, which is less useful to a job seeker than a reason would be.

## What came next

This project is the ancestor of [Verify This Job](https://github.com/TTHollis/VerifyThisJob), which addresses both limitations. There a language model is fine-tuned on the same underlying data so that it returns a verdict along with the specific phrases that triggered it, and an independent rule-based layer covers the modern scam patterns EMSCAD never saw. The two signals are combined conservatively, so either one can escalate a posting to a caution result.

## Files

| File | Contents |
|---|---|
| `fraud_classifier_final.ipynb` | Full pipeline: EDA, feature engineering, SMOTE, both models, threshold tuning, feature importance |
| `milestone3_eda_visuals.ipynb` | Exploratory analysis and the class balance, missingness, and structural feature charts |
| `milestone4_modeling.ipynb` | Modeling milestone, precursor to the final notebook |
| `fraud_classifier_paper.docx` | Written analysis |
| `fraud_classifier_presentation.pptx` | Presentation deck |
| `milestone*.docx` | Proposal, data selection, and interim reports |

## Running it

```bash
pip install pandas numpy scikit-learn imbalanced-learn nltk matplotlib seaborn
jupyter lab fraud_classifier_final.ipynb
```

The EMSCAD file (`fake_job_postings.csv`, about 48 MB) is not stored here. Download it from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction) into this folder before running the notebook.

## Reference

Vidros, S., Kolias, C., Kambourakis, G., & Akoglu, L. (2017). Automatic detection of online recruitment frauds: Characteristics, methods, and a public dataset. *Future Internet, 9*(1), 6. https://doi.org/10.3390/fi9010006
