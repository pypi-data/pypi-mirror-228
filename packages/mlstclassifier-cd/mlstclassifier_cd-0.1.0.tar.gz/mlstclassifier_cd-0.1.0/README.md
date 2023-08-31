# Overview

## MLST-based clade classifiers
Here I implemented different ML classifiers (KNN, RF) that take a Multi-Locus Sequence Type (MLST) file from strains of *C.difficile* or *C-difficile*-like and output a clade prediction (including cryptic clades). This is to make it easier and faster to predict a clade instead of doing it with phylogenetic tree building using STs. These classifiers are accurate at ~92%. I provided the pre-trained models of KNN and RF (.sav) for you to try them.
Inspired from StatQuest methodology (https://www.youtube.com/watch?v=q90UDEgYqeI&t=3327s).
I used the Scikit-learn library

## Steps:
- Load dataset: training and testing sets are from public PubMLST database of *C.difficile*.
- Apply GridSearchCV to find the best parameters (for KNN) or do pruning for RF.
- Train the classifier with best parameters.
- Predict clades on test set
- Print report and confusion matrix

## Usage:
The following libraries are necessary to run the script:
- sys
- pandas
- joblib

After downloading model.sav and MLST_classifier_EB.py and having your input file of MLST (see MLST_file_example.csv):
In the terminal write the following command:
```python3 MLST_classifier_EB.py path/to/input path/to/model.sav path/to/output```
