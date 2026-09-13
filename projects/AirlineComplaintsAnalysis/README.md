# Airline Complaints Analysis

Where, when, and why air travelers complain to the TSA, built as a six-visual briefing for the people who staff checkpoints. The analysis is as much about a change in how the data was collected as it is about the complaints themselves.

## The problem

TSA complaint data is published as PDF reports, which is to say it is public without being usable. The Data Liberation Project extracts it into tabular form. The question this analysis puts to that data is whether complaints concentrate predictably enough to staff against, which turns a reporting exercise into an operational argument.

The audience is TSA Office of Security Operations leadership and the Federal Security Directors running high-volume airports, who are already fluent in checkpoint terminology, so the visuals keep it rather than defining it.

## Data

Four files. Complaints by airport at 41,721 rows, by category at 241,588 rows, and by subcategory at 504,512 rows, all spanning January 2015 through January 2024, joined to an IATA/ICAO airport lookup of 8,937 rows for geography.

## The measurement problem

Airport attribution is not constant across the period. Roughly 45 to 50 percent of complaints name an airport from 2015 through 2020, rising to 59 percent in 2021 and 72 to 74 percent in 2022 and 2023. The cause is the TSA Contact Center's move to Salesforce at the end of 2020, which began populating the airport field.

This is the finding that shapes everything else. It means any airport-level or state-level view covering the full period would show a trend that is mostly an artifact of data collection. All geographic visuals are therefore restricted to 2022 and 2023, and one visual is built specifically to make the reporting change visible rather than hide it.

Other exclusions are documented rather than quietly applied. Fourteen airport codes could not be resolved to a U.S. location and are dropped, accounting for 1,131 complaints or 0.111 percent of the dataset. The subcategory file carries an asterisk placeholder where the source parser could not recover a name from the original PDF, covering 182,087 records or 73.2 percent of 2022-2023 subcategory rows. The District of Columbia has no airport in the lookup, so Reagan National and Dulles fall to Virginia and DC is rendered as no-data rather than as zero. U.S. territories fall outside the projection of a state choropleth, so their totals are annotated on the figure instead of being dropped.

## Findings

Complaints concentrate geographically. Five states, California, Florida, Texas, New York, and New Jersey, carry 107,372 complaints, 43.4 percent of the mapped total. The five busiest airports for complaints are Newark, Atlanta, Denver, JFK, and O'Hare.

Complaint load is not proportional to airport size. Grouping airports into volume tiers, the top tier of 34 airports behaves as a separate population whose median month exceeds the maximum month of the tier below. 258 airports sit under 100 complaints across two years.

What travelers complain about is shifting. Between 2022 and 2023 the largest share gain went to Procedures and Process at plus 3.16 points, and the largest drop to TSA PreCheck at minus 1.70.

The complaint mix varies by airport in ways that suggest local causes. O'Hare runs highest on Customer Service at 39.4 percent, Denver highest on Screening at 37.0 percent, and Los Angeles highest on Property Special Handling at 15.7 percent. Expedited Passenger Screening Program complaints are excluded from that comparison because they are handled centrally and would otherwise swamp the operational signal.

Volume rose sharply while the data was getting better at the same time. Mean monthly complaints went from 8,195 across 2015 to 2020 to 14,109 across 2022 to 2023, a 72 percent increase, while the attribution rate moved from 42 percent to 73 percent.

The operational recommendation that falls out of this is a targeted property handling and screening process intervention at the ten highest-volume airports, with Denver and Los Angeles prioritized because their complaint mix diverges most sharply from their peers.

## Design notes

Every chart title states the finding rather than the topic, following Knaflic's argument that the takeaway belongs in the headline. The palette is a colorblind-safe sequence of royal blue, amber, purple, forest green, and brown, with light gray reserved exclusively for absent or residual values so gray never competes with a data color. Category ordering is held constant across the stacked bars so the eye can track a single band horizontally instead of rereading each row.

## Files

| File | Contents |
|---|---|
| `airline_complaints_analysis.ipynb` | Full analysis: profiling, cleaning, geographic join, six visuals, summary paper |
| `complaints-by-airport.csv` | Complaint counts by airport and month |
| `iata-icao.csv` | Airport code to location lookup |
| `figures/` | The six exported visuals |

## Running it

```bash
pip install pandas numpy matplotlib seaborn geopandas
jupyter lab airline_complaints_analysis.ipynb
```

The category and subcategory files (about 17 MB and 73 MB) are not stored here. Download them from the [Data Liberation Project](https://github.com/data-liberation-project/tsa-complaint-counts) into this folder to reproduce visuals four and five.

## References

Data Liberation Project. (2023). *TSA complaint counts* [Data set]. GitHub. https://github.com/data-liberation-project/tsa-complaint-counts

IP2Location. (2024). *IATA/ICAO airport codes and locations* [Data set]. GitHub. https://github.com/ip2location/ip2location-iata-icao

Knaflic, C. N. (2015). *Storytelling with data: A data visualization guide for business professionals*. John Wiley & Sons.
