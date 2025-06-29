This repository contains files such as **code for mDepStar**, **PPI networks**, **reference complexes**, and **predicted protein complexes** used in the following research papers:

1. **Structural Asymmetries in PPI Networks as a Tool to Improve the Detection**  
   *Lukáš Papík, Eliška Ochodková¹, Eva Kriegová, Miloš Kudělka¹*  
   In: *Complex Networks & Their Applications XIII*, COMPLEX NETWORKS 2024, Volume 4, Springer Nature, 2025.

```bibtex
@inproceedings{papik2025structural,
  title={Structural Asymmetries in PPI Networks as a Tool to Improve the Detection},
  author={Papik, Lukas and Ochodkova$^1$, Eliska and Kriegova, Eva and Kudelka$^1$, Milos},
  booktitle={Complex Networks \& Their Applications XIII: Proceedings of The Thirteenth International Conference on Complex Networks and their Applications: COMPLEX NETWORKS 2024-Volume 4},
  volume={1190},
  pages={27},
  year={2025},
  organization={Springer Nature}
}
```


2. **Positive Impact of Structural Asymmetries in PPI Networks on Protein Complex Detection**  
   (manuscript under submission)

# mDepStar

Protein complex prediction method - Mutually Dependent Star

1. the dependencies of all adjacent node pairs (edges) are computed, and the dependency threshold $\tau$ is set;
2. each node is considered as a seed and together with all its mutually dependent neighbors as a predicted complex;
3. duplicate predictions are removed.

## Updates

- **29.06.** – As an **extended version**, the predicted complexes were added **together with updated code** for local threshold estimation.

## Project structure
- **mdepstar** mDepStar method source code
- **mdepstar_analysis** functions to calculate F-measure and MR-score
- **networks** giant component of each used PPI network
- **references** unprocessed references (CYC, SGD24) along with preprocessed references for each network, as described by the ClusterOne approach
- **predicted_complexes** sets of identified protein complexes in used protein-protein interaction (PPI) networks for each used method

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

for local version add parameter --local
```
mdepstar networks/ppi-network -l -o predictions -w
```

For more information, such as setting a custom dependency threshold or predicting a complex for only one selected protein, use:
```
mdepstar -h
```
