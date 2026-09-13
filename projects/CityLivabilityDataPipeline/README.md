# City Livability Data Pipeline

Three public data sources, three different geographic levels, one queryable database and a composite livability score for 2,309 U.S. counties.

## The problem

Deciding where to live means weighing things that are published separately and never line up. Housing costs come from HUD, walkability and transit come from Walk Score, and income, poverty, education, and commute times come from the Census. Each is useful alone and none of them answers the actual question, which is where a person can afford to live and still get around.

This project builds the join. It is less about modeling than about the unglamorous work that has to happen before any model is possible: acquiring data from a flat file, a scraped web page, and an API, reconciling identifiers that do not match, and landing the result somewhere it can be queried.

## Data sources

HUD Fair Market Rent, published as a county-level flat file, giving rent benchmarks by bedroom size. Walk Score city rankings, scraped from the live HTML table at walkscore.com, giving walkability, transit, and bike scores. Census American Community Survey 5-Year Estimates for 2022, pulled from the public Census API, giving population, median household income, poverty counts, educational attainment, and commute times for all 3,000-plus counties. The ACS endpoint used here needs no API key, which keeps the notebook reproducible without exposing credentials.

## The interesting problem

The three sources do not share a geographic level. HUD publishes below the county line, Walk Score publishes by city, and the Census publishes by county. There is no single key that joins all three.

The resolution is two different strategies in one pipeline. Census and HUD are joined on a FIPS code assembled by padding the state code to two digits and the county code to three, which is an exact inner join. Walk Score has no FIPS code at all and no clean city-to-county mapping, so it is aggregated to the state level and joined on state, which is a deliberate loss of precision documented as a limitation rather than hidden. The result is 4,276 county rows across 43 states, of which 2,309 have complete data across all three sources.

## Cleaning

Each source needed different work, and the counts are reported rather than asserted. HUD arrived nearly clean, requiring no header, name, or type corrections, though 213 outliers were flagged in two-bedroom rents using the IQR method and kept rather than dropped, since expensive counties are real. Walk Score, being scraped, needed six headers standardized to snake case, two UTF-8 garbled city names repaired, 130 values coerced to numeric, and 22 Canadian cities identified and separated out. The Census extract returns every value as a string, so seven numeric fields were converted, 3,063 county names had their "County" and "Parish" suffixes stripped, and state names were mapped to USPS abbreviations with zero left unmapped.

Everything lands in a SQLite database (`city_livability.db`) as three tables, and all joins and analysis run as SQL queries against it rather than as in-memory merges.

## Quality of Life Index

A composite score, min-max scaled to 0 to 1 per component and then weighted:

| Component | Weight | Direction |
|---|---|---|
| Median household income | 25% | Higher is better |
| Walk Score | 20% | Higher is better |
| Transit Score | 20% | Higher is better |
| Two-bedroom fair market rent | 15% | Lower is better |
| Poverty count | 10% | Lower is better |
| Education rate | 10% | Higher is better |

The weights are a judgment call, not a finding, which is the honest thing to say about any composite index. Counties missing Walk Score coverage receive a null score rather than an imputed one.

## What it shows

Rent tracks income, which is unsurprising, but the relationship is not uniform: eight states sit well below the income line their walkability would predict, and three exceed it. Fair market rent climbs steadily with bedroom count, from roughly $800 for a studio to just under $1,800 for a four-bedroom nationally, which is where family housing burden becomes visible. On the composite index, northeastern states lead on the strength of transit and walkability relative to income, while southern and rural states score lower largely on transportation access.

Six visualizations carry the analysis, one built in Python and five in Power BI, ranging from a filled map of rents by state to a bubble chart of income against rent sized by population.

## What came next

The county-level version of this question became [QRoots](https://github.com/TTHollis/QRoots), a deployed application that scores census tracts rather than counties, adds crime and education data, and lets a user reweight the index themselves instead of accepting my weights. The pipeline here is where that idea was proven out.

## Files

| File | Contents |
|---|---|
| `city_livability_pipeline.ipynb` | Full pipeline: acquisition, cleaning, SQLite load, SQL joins, index, visualizations |
| `city_livability.db` | SQLite database with the three cleaned tables |
| `city_livability_dashboard.pbix` | Power BI dashboard |
| `term_project_notebook.ipynb` | Earlier milestone work |
| `milestone1_proposal.docx` | Project proposal |
| `hud_*.csv`, `merged_*.csv`, `qol_ranked.csv` | Cleaned and merged intermediate datasets |
| `Viz*.png` | Exported dashboard visuals |

## Running it

```bash
pip install pandas numpy requests beautifulsoup4 matplotlib seaborn
jupyter lab city_livability_pipeline.ipynb
```

The notebook scrapes Walk Score live and calls the Census API, so both need network access and the scrape may need adjusting if the site's markup has changed since. The Power BI file requires Power BI Desktop.

## References

U.S. Census Bureau. (2022). *American Community Survey 5-year estimates* [Data set]. https://api.census.gov/data/2022/acs/acs5

U.S. Department of Housing and Urban Development. (2024). *Fair market rents* [Data set]. https://www.huduser.gov/portal/datasets/fmr.html

Walk Score. (2026). *Cities and neighborhoods* [Data set]. https://www.walkscore.com/cities-and-neighborhoods/
