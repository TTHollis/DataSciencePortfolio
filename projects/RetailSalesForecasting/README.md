# Retail Sales Forecasting

Forecasting monthly U.S. retail sales with a seasonal regression baseline and a SARIMA model, and a test window that happens to land on one of the worst possible periods to forecast.

## The problem

Monthly retail sales drive inventory, staffing, and capital planning. The series has a strong upward trend and a hard December seasonal peak, which makes it a natural candidate for both a regression-with-seasonal-dummies approach and a classical time series model. The interesting question is what happens when a structural break sits inside the test window.

## Data

U.S. monthly retail sales, January 1992 through June 2021, reshaped from a year-by-month wide table into 354 monthly observations. Training covers January 1992 through June 2020, 342 months. The test set is the final 12 months, July 2020 through June 2021.

## Approach

The baseline is a linear regression on a time index plus eleven monthly dummy variables, which fits the trend and the seasonal shape together and achieves an R-squared of 0.979 on the training data.

SARIMA is the comparison, chosen because it learns autocorrelation and seasonality directly from the series rather than having the seasonal structure imposed on it by dummy variables.

## Results

| Model | Test RMSE | Error as share of mean actual |
|---|---|---|
| Linear regression with seasonal dummies | $66,598 million | 12.9% |
| SARIMA | $59,819 million | 11.6% |

SARIMA reduces error by about $6,779 million, roughly a 10 percent improvement over the baseline.

## What the residuals say

All twelve test residuals are positive. The model does not scatter around the truth, it sits below it, and the gap widens over time, reaching more than $107 billion by March through June 2021.

That is not a modeling defect so much as a description of what happened. The test window covers the COVID-19 recovery, when stimulus payments and pent-up demand produced a level of consumer spending that has no precedent in twenty-eight years of training data. Neither model could have anticipated it, because the information was not in the series.

The honest read is that both models are well specified for normal conditions and that the RMSE figures here measure the size of a structural break as much as they measure model quality. SARIMA is the better choice going forward, though the residual plot is the part of this project worth looking at, because it shows what a forecast failure caused by a regime change looks like as opposed to one caused by a bad model.

## Files

| File | Contents |
|---|---|
| `retail_sales_forecasting.ipynb` | Full analysis: reshaping, visualization, both models, residual diagnostics, RMSE comparison |
| `us_retail_sales.csv` | Source series |
| `retail_sales_plot.png` | The series over time |
| `retail_sales_predictions.png` | Predicted against actual across the test window |
| `residual_plot.png` | Residual diagnostics showing the systematic underestimation |
| `sarima_comparison.png` | Baseline against SARIMA |

## Running it

```bash
pip install pandas numpy scikit-learn statsmodels matplotlib seaborn
jupyter lab retail_sales_forecasting.ipynb
```

All data needed is included in this folder.
