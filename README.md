# mDepStar

Protein complex prediction method - Mutually Dependent Star

1. the dependencies of all adjacent node pairs (edges) are computed, and the dependency threshold $\tau$ is set;
2. each node is considered as a seed and together with all its mutually dependent neighbors as a predicted complex;
3. duplicate predictions are removed.

## Project structure
- **mdepstar** mDepStar method source code
- **mdepstar_analysis** functions to calculate F-measure and MR-score
- **networks** giant component of each used PPI network
- **references** preprocessed references for each network, as described by the ClusterOne approach

## Installation
From the project root:
```
pip install .
```

## Usage
To predict complexes on a weighted (-w) PPI network and output the results to a file (-o) named predictions_clusters.txt, where each line contains a predicted protein complex with proteins delimited by a space, use:
```
mdepstar networks/ppi-network -o predictions -w
```
For more information, such as setting a custom dependency threshold or predicting a complex for only one selected protein, use:
```
mdepstar -h
```
