# Rain Prediction in Australia

Predicts whether it will rain tomorrow from daily weather observations, using a decision tree and k-nearest neighbours (scikit-learn).

*Developed with Afonso Cordeiro. Course: Machine Learning, University of Coimbra, 2022/23 (first challenge).*

## Dataset

[Rain in Australia](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package) (Kaggle): 145,460 daily observations from 49 Australian weather stations between 2007 and 2017. The target is `RainTomorrow` (rain of 1 mm or more). The dataset is not included in this repository.

## Approach

1. **Pre-processing:** rows with missing values are dropped (56,420 remain), categorical columns (date, location, wind directions) are encoded with `pd.factorize`, and Yes/No columns become 1/0.
2. **Feature selection:** correlation with `RainTomorrow`. The five features with |r| > 0.3 are kept: `Humidity3pm` (0.46), `Sunshine` (−0.45), `Cloud3pm` (0.39), `Cloud9am` (0.32) and `RainToday` (0.31).
3. **Models:** decision tree (entropy criterion) and KNN (k = 21), each trained and tested on 30 random 75/25 splits.

## Results

Mean accuracy over the 30 splits:

| Model | Train | Test |
|---|---|---|
| Decision tree | 97.7% | 77.3% |
| KNN (k = 21) | 84.3% | 83.3% |

For comparison, always predicting "no rain" gives 78% accuracy on this data.

The notebook keeps all its outputs (correlation heatmap, tree, confusion matrices), so it can be read directly on GitHub. The report is in [report-pt.pdf](report-pt.pdf) (Portuguese).

## How to run

The notebook was written for Google Colab: put `weatherAUS.csv` in a folder called `AC` in your Google Drive and run all cells. To run it locally, remove the `drive.mount` cell and change the path in `pd.read_csv`.

It needs the library versions from that time, pinned in [requirements.txt](requirements.txt): from scikit-learn 1.4 onwards, `accuracy_score` returns a plain `float`, and the notebook's `.round()` calls fail.

## Known limitations

- The decision tree overfits (97.7% train vs. 77.3% test), and its test accuracy is below the 78% obtained by always predicting "no rain".
- Only accuracy is reported, even though the classes are imbalanced (22% rainy days). Precision and recall for rainy days would say more.
- Dropping every row with a missing value discards 61% of the data.
- The features are selected with correlations computed on the full dataset, before the train/test split.
