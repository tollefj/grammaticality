import conllu
import numpy as np

from dataclasses import dataclass
from tqdm import tqdm

def read_ud(split="train"):
    path = f"../../UD/no_bokmaal-ud-{split}.conllu"
    with open(path, "r", encoding="utf-8") as f:
        data = conllu.parse(f.read())
    parsed_sents = []  # triple of (pos, form, head)
    for sentence in data:
        tmp = []
        for token in sentence:
            tmp.append(token["upostag"])
            # tmp.append((token["upostag"], token["form"], token["head"]))
        parsed_sents.append(tmp)
        # parsed_sents.append(np.asarray(tmp))
    # parsed_sents = np.asarray(parsed_sents)
    return parsed_sents

@dataclass
class TrainableData:
    X: np.ndarray
    y: np.ndarray

def get_trainable_data(split: str, pos_map: dict) -> TrainableData:
    print(f"Reading {split} data")
    parsed_sents = read_ud(split)
    percentile = np.percentile([len(s) for s in parsed_sents], 95)
    sents = [s for s in parsed_sents if len(s) <= percentile]
    MAX_LEN = len(max(sents, key=len))

    def scramble_np_sequence(seq):
        seq = np.asarray(seq)
        return np.random.permutation(seq)
    
    def pad(seq):
        return np.pad(seq, (0, MAX_LEN - len(seq)), constant_values="UNK")
    def vec(seq):
        return np.vectorize(pos_map.get)(seq)

    RATIO = 20
    all_sents = np.zeros((len(sents) * (RATIO + 1), MAX_LEN), dtype=np.int32)
    all_labels = np.zeros((len(sents) * (RATIO + 1),), dtype=np.int32)
    
    print(f"Scrambling sentences, padding and converting...")
    for i, sent in tqdm(enumerate(sents)):
        for j in range(RATIO):
            scrambled = vec(pad(scramble_np_sequence(sent)))
            all_sents[i * (RATIO + 1) + j] = scrambled
            all_labels[i * (RATIO + 1) + j] = 0

        all_sents[i * (RATIO + 1) + RATIO] = vec(pad(sent))
        all_labels[i * (RATIO + 1) + RATIO] = 1
        
    return TrainableData(X=all_sents, y=all_labels)