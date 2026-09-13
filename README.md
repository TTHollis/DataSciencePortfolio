# Data Science Portfolio

Graduate data science work by Tim Hollis: end-to-end projects in fraud detection, forecasting, recommendation, data pipelines, and visual storytelling, plus the coursework behind them. Everything here runs in Python (pandas, scikit-learn, statsmodels, matplotlib, seaborn) and, where noted, Power BI.

Deployed applications live in their own repositories and are linked below.

## Projects

| Project | What it does | Methods |
|---|---|---|
| [Verify This Job](https://github.com/TTHollis/VerifyThisJob) | Fine-tuned LLM that flags fraudulent job postings and explains the red flags, deployed as a Streamlit app with a rule-based safety net. [Live app](https://verifythisjob.streamlit.app) | Full fine-tune of Qwen2.5-0.5B, Hugging Face Transformers, Streamlit |
| [Job Posting Fraud Classifier](projects/JobPostingFraudClassifier) | Classical ML predecessor to Verify This Job: predicts fraudulent postings from text and structural features on the EMSCAD dataset, tuned for recall | TF-IDF, SMOTE, logistic regression, random forest, threshold tuning |
| [Billboard Hit Prediction](projects/BillboardHitPrediction) | Predicts whether a song reaches the Billboard Hot 100 top 10 from lyrical features such as sentiment, length, and repetitiveness | NLP feature engineering, random forest (AUC-ROC 0.778), logistic regression |
| [City Livability Data Pipeline](projects/CityLivabilityDataPipeline) | Cleans and merges HUD fair market rents, Walk Score rankings, and Census data into a SQLite database, then visualizes cost of living and quality of life across U.S. cities. The groundwork for QRoots | Web scraping, API ingestion, data cleaning, SQLite, Power BI |
| [QRoots](https://github.com/TTHollis/QRoots) | Relocation guide that scores U.S. census tracts on crime, education, income, housing, and quality of life. [Live app](https://qroots.onrender.com) | React, Python, Census API, SHAP explanations |
| [Childcare Affordability in Texas](projects/ChildcareAffordabilityTexas) | Data story on the childcare affordability gap and its effect on second-earner decisions, delivered as a briefing deck, dashboard, and infographic | Visual storytelling, parallel coordinates, dashboard design |
| [Retail Sales Forecasting](projects/RetailSalesForecasting) | Forecasts monthly U.S. retail sales and compares a baseline model against SARIMA with residual analysis and RMSE | Time series analysis, SARIMA, train/test evaluation |
| [Airline Complaints Analysis](projects/AirlineComplaintsAnalysis) | Where, when, and why air travelers complain, joined to airport geography and visualized as a six-chart narrative | Geographic joins, choropleth, seasonality heatmap, slope and dumbbell charts |
| [Hybrid Movie Recommender](projects/HybridMovieRecommender) | Combines content-based genre and tag similarity with SVD collaborative filtering on MovieLens | Cosine similarity, matrix factorization, hybrid scoring |
| [Vagari Vita](https://github.com/TTHollis/VagariVita) | Local event discovery and AI-generated cultural travel briefings as a progressive web app. [Live app](https://vagarivita.onrender.com) | React PWA, FastAPI, LLM integration |

Two capstone projects are in progress. The first extends the job posting fraud work above with unsupervised methods, and will be folded into the Verify This Job entry as it develops. The second will be added here once complete.

## Coursework

Weekly exercises and smaller assignments, grouped by subject. These show the breadth of the program; the projects above are the depth.

| Folder | Subject | Course |
|---|---|---|
| [IntroductionToProgramming](coursework/IntroductionToProgramming) | Python fundamentals | DSC510 |
| [StatisticsForDataScience](coursework/StatisticsForDataScience) | Statistics in R | DSC520 |
| [DataExplorationAndAnalysis](coursework/DataExplorationAndAnalysis) | EDA, distributions, hypothesis testing | DSC530 |
| [DataPreparation](coursework/DataPreparation) | Cleaning, wrangling, APIs, SQL | DSC540 |
| [DataMining](coursework/DataMining) | Feature engineering, classification, clustering, neural networks | DSC550 |
| [PredictiveAnalytics](coursework/PredictiveAnalytics) | Regression, time series, recommenders, model evaluation | DSC630 |
| [DataPresentationAndVisualization](coursework/DataPresentationAndVisualization) | Data storytelling, infographics, dashboards | DSC640 |
| [AdvancedGenerativeAI](coursework/AdvancedGenerativeAI) | Prompting, RAG, fine-tuning, LLMOps | DSC670 |
| [AppliedDataScience](coursework/AppliedDataScience) | Capstone projects | DSC680 |

## Repository layout

```
projects/       showcase projects, one folder each with a README, notebook, figures, and small data
coursework/     weekly exercises grouped by subject
```

## Running the notebooks

Each notebook lists its imports in a single setup cell. A conda environment with pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn, and jupyterlab covers nearly everything; individual project READMEs note anything extra.

Datasets over 10 MB are not stored in this repository. Where a notebook depends on one, its README links to the original source so the data can be downloaded into the project folder.

## Author

Tim Hollis · [GitHub profile](https://github.com/TTHollis) · [LinkedIn](https://www.linkedin.com/in/timothy-hollis)
