""" Nepusz, T., Yu, H. & Paccanaro, A., 2012. Detecting overlapping protein complexes in protein-protein
    interaction networks. Nature Methods, Volume 9, pp. 471-472."""

from .mwmatching import maxWeightMatching

def overlap_score(set1, set2):
    return len(set1.intersection(set2)) ** 2 / (float(len(set1)) * len(set2))

def maximum_matching_ratio(reference, predicted, score_threshold=0.25):
    scores = {}
    n = len(reference)
    if n == 0:
        return 0
    
    for id1, c1 in enumerate(reference):
        for id2, c2 in enumerate(predicted):
            score = overlap_score(c1, c2)
            if score > score_threshold:
                scores[id1, id2+n] = score
            
    inpt = [(v1, v2, w) for (v1, v2), w in scores.items()]
    
    mates = maxWeightMatching(inpt)
    score = sum(scores[i, mate] for i, mate in enumerate(mates) if i < mate)
    return score / n
    

def predictive_matching_ratio(reference, predicted, threshold=0.25):
    res = []
    for id1, c1 in enumerate(predicted):
        os_vals = []
        for id2, c2 in enumerate(reference):

            score = overlap_score(c1, c2)
            os_vals.append(score)
        m = max(os_vals)
        if m > threshold:
            res.append(m)

    return sum(res) / len(predicted)

def precision(reference, predicted, threshold=0.25):
    counter = 0
    for pred in predicted:
        for ref in reference:
            score = overlap_score(ref, pred)
            if score > threshold:
                counter += 1
                break
    return counter / float(len(predicted))


def recall(reference, predicted, threshold=0.25):
    counter = 0
    for ref in reference:
        for pred in predicted:
            score = overlap_score(ref, pred)
            if score > threshold:
                counter += 1
                break
    return counter / float(len(reference))

def F_measure(p, r): # / MR-score
    if r == 0 and p == 0:
        return 0
    return (2 * p * r) / (p + r)
