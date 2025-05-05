# Soteria Initiative Monitoring Methodology

The data collection is against public [sources](../data/data_sources.csv) with the intend to proxy
the FATF Immediate Outcome statements as described below.

| Metric Name                              | Immediate Outcome | Outcome Description                                            |
| ---------------------------------------- |-------------------|----------------------------------------------------------------|
| FATF Rating                              | -                 | Target: Assumed to be the result of a change in other metrics. |
| Number of SARs/STRs                      | IO.6              | Financial intelligence: quantity of STRs received.             |
| SARs/STRs per Capita                     | IO.6              | Financial intelligence: STR coverage relative to population.   |
| Fine Volume                              | IO.3              | Supervision: enforcement action via monetary sanctions.        |
| Fine Volume Inflation-Adj. % of GDP      | IO.3              | Supervision: scale of sanctions relative to economic size.     |
| Fine Count                               | IO.3              | Supervision: number of enforcement actions.                    |
| Fine Count per Capita                    | IO.3              | Supervision: sanction frequency relative to population.        |
| Recovered Assets                         | IO.9              | Confiscation: value of assets frozen/seized/recovered.         |
| Recovered Assets Inflation-Adj. % of GDP | IO.9              | Confiscation: recovery effort relative to economic size.       |
| Conviction Count                         | IO.8              | ML prosecution: number of convictions secured.                 |
| Convictions per Capita                   | IO.8              | ML prosecution: conviction rate relative to population.        |
| Inflation                                | –                 | Control variable (not a proxy for an Immediate Outcome).       |
| Annual GDP                               | –                 | Control variable (not a proxy for an Immediate Outcome).       |

Each metrics is scaled to the economy of the country either using population or inflation adjusted GDP figures.
The data sources for the metrics have been selected with the following rationales.

| Metric Name                           | Source Name                                 | Source Link                                                                                                      | Justification                                                                                                                                                 |
| ------------------------------------- |---------------------------------------------|------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FATF Rating                           | Basel Index – Basel Institute of Governance | [https://index.baselgovernance.org/downloads](https://index.baselgovernance.org/downloads)                       | The Basel Index weights FATF with 50% and is an independently calculated country-level FATF‐style ratings across jurisdictions.                               |
| Number of SARs/STRs                   | FIU Reports                                 | [Per country](../data/data_sources.csv)                                                                          | Annual FIU reports are the official publication of all SAR/STR counts, ensuring consistency and comparability year-to-year for that country.                  |
| SARs/STRs per Capita                  | World Bank Population (total)               | [https://data.worldbank.org/indicator/SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL)             | Population totals from the World Bank allow conversion of raw SAR counts into per-capita figures on a consistent, global basis.                               |
| Fine Volume                           | Violation Tracker Global                    | [https://violationtrackerglobal.goodjobsfirst.org](https://violationtrackerglobal.goodjobsfirst.org)             | Violation Tracker aggregates corporate enforcement data worldwide and is the most comprehensive source for monetary fines levied under AML/CFT regimes.       |
| Fine Volume (Inf.-Adj. % of GDP)      | World Bank GDP (Current USD)                | [https://data.worldbank.org/indicator/NY.GDP.MKTP.CD](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)       | Current-USD GDP figures from the World Bank allow standardizing fine volumes relative to economic size, adjusting for inflation via separate deflator series. |
| Fine Count                            | Violation Tracker Global                    | [https://violationtrackerglobal.goodjobsfirst.org](https://violationtrackerglobal.goodjobsfirst.org)             | Alongside volumes, Violation Tracker also reports counts of enforcement actions, making it the go-to for sanction frequency.                                  |
| Fine Count per Capita                 | World Bank Population (total)               | [https://data.worldbank.org/indicator/SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL)             | Population data is needed to express number of fines in per-person terms, for cross-country comparability.                                                    |
| Recovered Assets                      | FIU Reports                                 | [https://www.argentina.gob.ar/uif/informes-de-gestion](https://www.argentina.gob.ar/uif/informes-de-gestion)     | Argentina’s UIF reports include official figures on assets recovered under AML/CFT powers, the primary national source for this metric.                       |
| Recovered Assets (Inf.-Adj. % of GDP) | World Bank GDP (Current USD)                | [https://data.worldbank.org/indicator/NY.GDP.MKTP.CD](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)       | Using consistent GDP data allows expressing recovered assets as a share of the economy, controlling for country size.                                         |
| Conviction Count                      | FIU Reports                                 | [Per country](../data/data_sources.csv)                                                                          | Annual FIU reports are the official publication of all SAR/STR counts, ensuring consistency and comparability year-to-year for that country.                  |
| Convictions per Capita                | World Bank Population (total)               | [https://data.worldbank.org/indicator/SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL)             | Population data permits normalization of conviction counts to per-capita rates.                                                                               |
| Inflation                             | World Bank Inflation (GDP deflator annual)  | [https://data.worldbank.org/indicator/NY.GDP.DEFL.KD.ZG](https://data.worldbank.org/indicator/NY.GDP.DEFL.KD.ZG) | The World Bank’s GDP deflator series is the standard for adjusting monetary values for inflation across countries.                                            |
| Annual GDP                            | World Bank GDP (Current USD)                | [https://data.worldbank.org/indicator/NY.GDP.MKTP.CD](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)       | Current-USD GDP figures from the World Bank are the most widely used baseline for economic-size comparisons and denominator calculations (e.g. fines/GDP).    |

The FATF Rating will be assessed for correlations in a cross-sectional and timeseries analysis to other metrics
in so far as the sparse dataset allows to draw meaningful conclusions.
