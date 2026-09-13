# Childcare Affordability in Texas

A persuasive data story built for state legislators: childcare in Texas fails the federal government's own affordability standard in every county that reports, and the household math now forces families to ask whether a second income still pays for itself.

## The problem

The U.S. Department of Health and Human Services considers childcare affordable when it costs no more than 7 percent of household income. That benchmark is the spine of this project, because it lets a policy argument rest on the government's own standard rather than on an advocacy group's.

The audience is Texas state legislators and their staff: policy literate but not data literate, and carrying a fiscal skepticism toward new spending that the story has to earn its way past rather than ignore. The ask is specific, which is to expand state childcare subsidy funding and raise the income eligibility ceiling so that families above the current cutoff but far below affordability are not left out.

## Data

The National Database of Childcare Prices, published by the U.S. Department of Labor Women's Bureau, at 34,567 county-year records spanning 2008 through 2018 across 51 jurisdictions and 227 columns. The analysis narrows to identifiers, median weekly center-based infant and preschool prices, median household income, and female median earnings. Weekly prices are annualized at 52 weeks and measured against the 7 percent standard.

## Findings

Childcare fails the federal standard almost universally. In 2018 only 4 of 2,360 reporting counties nationwide came in at or below 7 percent, the median county spent 16.1 percent of household income on care for a single infant, and zero of 254 Texas counties met the standard.

The burden grew across the decade. The national median county moved from 15.4 percent in 2008 to 16.1 percent in 2018, and Texas from 13.3 percent in 2009 to 14.5 percent in 2018, while the broader economy was recovering.

The household math is severe. One infant in center-based care consumes 33.2 percent of female median earnings in the typical county and 31.7 percent in Texas. An infant and a preschooler together consume 61.1 percent nationally and 58.3 percent in Texas. Bexar County, where I live, sits at $8,666 per year for infant care, or 33.1 percent of female median earnings.

The Texas failure is not a near miss at the margin. Of 254 counties, 101 fall between 7 and 14 percent, and the rest sit higher.

## Three mediums, three speeds

Each medium carries its own visuals rather than resized copies of a shared set.

The PowerPoint briefing deck is the slow version, arguing at national scale: the federal standard, the 2018 distribution, the decade trend, the second-earner comparison, and state medians, with the ask arriving last.

The Power BI dashboard is the self-serve version and the only medium working at county granularity, keeping all 254 Texas counties visible across four panels: every county plotted individually, price against income, the spread within each reporting year, and the ten counties carrying the heaviest burden.

The infographic is the fast version and uses no conventional chart at all. An icon array stands in for the 254 counties, a part-to-whole bar shows what remains of a mother's earnings after care, and a bullet chart measures the Texas median against the benchmark.

## Ethics and limitations

No imputation was added. County-years missing infant price or income were dropped, removing about 32 percent of rows, and that figure is disclosed alongside any trend claim. Derived fields are limited to annualized cost and income share, with no outlier removal and no smoothing.

The real risks live in the transformations, and the notebook states them. Assuming 52 weeks of care overstates cost for part-year arrangements. Comparing full-time care prices against earnings that include part-time workers inflates the earnings-share figures. Dropping non-reporting counties biases the sample toward larger and more urban places, which runs directly against one of the visuals, since the ten most burdened Texas counties are all small rural ones, exactly where sample sizes are smallest.

The framing carries risk too. The story could imply that childcare prices cause mothers to leave the workforce, which the correlation in this data does not support, and pricing care against a mother's earnings encodes an assumption about which parent is the second earner. The mitigations are to footnote assumptions where they appear, report the null correlation openly, keep axes zero-based, and disclose that only 41 jurisdictions reported 2018 prices.

## Files

| File | Contents |
|---|---|
| `childcare_affordability_story.ipynb` | Final term project: analysis, all three mediums, summary paper, ethics assessment |
| `milestone1_findings.ipynb` | Initial findings and the affordability gap |
| `milestone2_visuals.ipynb` | Visualization development |
| `milestone3_mockups.ipynb` | Medium mock-ups |
| `milestone4_review.ipynb` | Peer review and revision |
| `viz_parcoords_childcare_tx.png` | Parallel coordinates view of Texas counties |

## Running it

```bash
pip install pandas numpy matplotlib seaborn openpyxl
jupyter lab childcare_affordability_story.ipynb
```

The source file (`nationaldatabaseofchildcareprices.xlsx`, about 27 MB) is not stored here. Download it from the [Women's Bureau](https://www.dol.gov/agencies/wb/topics/featured-childcare) into this folder first.

## Reference

U.S. Department of Labor, Women's Bureau. (2024). *National database of childcare prices* [Data set]. https://www.dol.gov/agencies/wb/topics/featured-childcare
