# MLSTclassifier_cd

## Table of Contents

- [Overview](#overview)

- [Installation](#installation)

- [Usage](#usage)

- [Output](#output)

## Overview

Enhance your clade prediction process with MLSTclassifier_cd, a powerful machine learning tool that employs K-Nearest Neighbors (KNN) algorithm. Designed specifically for Multi-Locus Sequence Type (MLST) analysis of _C.difficile_ strains, including cryptic variants, this tool streamlines and accelerates clade prediction. MLSTclassifier_cd achieves accuracy of approximately 92% for predictions.

StatQuest methodology was used to build the model (https://www.youtube.com/watch?v=q90UDEgYqeI&t=3327s). Powered by the Scikit-learn library, MLSTclassifier_cd is a good tool to have a first classification of your _C.difficile_ strains including cryptic ones.

GitHub repo: https://github.com/eliottBo/MLSTclassifier_cd

## Installation:

**Install PyPI package:**

`pip install mlstclassifier-cd`

## Usage:

### Basic Command:

The query csv file must have the same structure as the example "MLST_file_example.csv".

`MLSTclassifier_cd [query csv file path] [output path]`

## Output:

After running MLSTclassifier_cd, the output file should contain an additional column named "predicted_clade"