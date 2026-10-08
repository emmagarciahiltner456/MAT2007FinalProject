# MAT2007FinalProject
Coronary Heart Disease Analysis
This project uses the Cleveland Heart Disease dataset to compare five clinical traits and determine which are most strongly related to the presence and increasing category of coronary heart disease (CHD).

Research questions
-> Which clinical trait best distinguishes patients with and without CHD?
-> Which clinical trait has the strongest relationship with increasing CHD category?

Dataset
-> Source: UCI Machine Learning Repository
https://archive.ics.uci.edu/dataset/45/heart+disease
-> File used: processed.cleveland.data
- Included: 303 patients and 14 variables
*Missing values shown as ? are read as NA in R

What the scripts do:
FINAL_ANALYSIS.r
- Loads and prepares the Cleveland dataset
- Tests age, resting blood pressure, serum cholesterol, maximum heart rate, and ST depression
- Uses logistic regression and AUC to compare CHD presence
- Uses Spearman correlation to compare CHD category
- Calculates 95% confidence intervals

- Exports:
  - heart_disease_results.txt
  - heart_scatter_data.txt

FINALGRAPHS.py
Creates:
- AUC_python.png
- Severity_python.png
- Scatter_python.png

Dependencies:
R
- pROC
-> Install with: install.packages("pROC")

Python
- pandas
- matplotlib
- numpy
Install with:
pip install pandas matplotlib numpy

How to run:
1. Download processed.cleveland.data.
2. Put the dataset and both scripts in the same project folder.
3. Update the file paths in the R and Python scripts for your computer.
4. Run the R script first: (make sure to change the loading saving section - on line 12 and from line 219, to match file locations on own computer)
  Rscript FINAL_ANALYSIS.r
5. Then run the Python script:
  python3 FINALGRAPHS.py
*The R script must be run first because it creates the text files used by Python.
