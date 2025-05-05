# About the Project
The Monitoring project is part of the [Soteria Initiative](https://soteria-initiative.org/) to establish common financial
crime data standards and has been established to measure AML/CTF & Sanction Controls framework improvements.

Establishing status quo and measuring progress is vital. Even while the Soteria Initiative advocates for controlled-population
based metrics (e.g., red-teaming) for a true learning loop, the outcome based metrics still provide vital information
about trends towards an improved AML/CTF framework. For that purpose this monitoring project identifies and collects 
proxy measures for FATF Immediate Outcome (IOs) items that are observable to the public. 

For that purpose we consider not only the FATF IOs but also the data collection and measurement methodology:
- [FATF Immediate Outcome Assessment Methodology](https://www.fatf-gafi.org/content/dam/fatf-gafi/methodology/FATF-Assessment-Methodology-2022.pdf.coredownload.inline.pdf)
- [Soteria Initiative Monitoring Methodology](documentation/methodology.md)
- [Soteria Initiative data source referencs](data/data_sources.csv)

The monitoring project is work in progress. Collecting all data points is challenging because many of the metrics 
are either not published, not published regularly, published as pictures only, measured in different dimensions 
(all kind fo SARs vs just AML related SARs) or over different measurement time frames (e.g., quarterly vs bi-annual).
Help is required hence both to review, adjust and improve the 
[measurement methodology](documentation/methodology.md) 
as well as to identify [data sources](data/data_sources.csv)
and validate the [report results](reports/20250505_report_data.csv). 

Please consider [contributing](#contributing)!

# 🕹 Getting Started
1. Clone the repo
```zsh
git clone https://github.com/SoteriaInitiative/monitoring.git
cd monitoring
```
2. Install the required dependencies
```zsh
brew install tesseract

pip install -r requirements.txt
```
3. Run data collection & report generation

First run the data collection. This will use the sources in ``data/data_sources.csv`` to
generate a data set for the report in ``reports/<YYYYMMDD_report_data.csv``:
```zsh
python implementation/data_collector.py
```

To run the report analytics and summary report creation run the report generator:
```zsh
python implementation/report_generator.py
```
> NOTE: Data and reports are only versioned daily and old files for the day will be overwritten with new ones.

4. Review the results
You can find the report in the ```reports/``` directory. 


# 🗄️ Project Structure
To find your way around please find a quick overview of the project structure.
```
coredata/
├── data/               # Inputa data source references
├── documentation/      # Data collection methodology and analysis considerations
├── implementation/     # Data collection and analytics implementation
├── reports/            # Resulting data files and summaries
├── README.md           # This file
└── LICENSE             # License file
```
# 🛠️ Contributing
Contributions are welcome! To get started:

1. Fork the project. 
2. Create an issue to work on at git-hub
2. Create a new feat, doc or std branch (replace feat with doc or std): git checkout -b feat/<issue-#>-<change>. 
3. Commit your changes: git commit -m 'Commit message'. 
4. Push to your branch: git push origin feat/<issue-#>-<change>. 
5. Open a pull request in the main repository.

# 🚀 Features

This release includes the following key features:
- A list of data sources for FIU
- An initial methodology description
- Data collection and extraction for FATF Ratings
- Manual seed data of baseline SAR counts for selected countries

# ⚠️ Limitations:
Please consider the following limitations or known issues:
- FATF Rating extraction is still unreliable and lacks source link inclusion
- Several countries missing in data report
- No correlation reports are generated
- Most metrics remain empty
- 
# 📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute this project as per the terms of the license.
# 📬 Contact
Project Maintainer: Soteria Initiative – @SoteriaInitiative – contact@soteria-initiative.org
Repository: SoteriaInitiative/monitoring
For general inquiries or discussion, please open an issue.