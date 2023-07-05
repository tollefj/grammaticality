import pandas as pd
from typing import List, Tuple

PATH = "../data/nocola_parsed"

def get_df(split: str = "train") -> pd.DataFrame:
    dataset_path: str = f"{PATH}/nocola_ungrammatical_{split}.txt"
    data: List[Tuple[str, str]] = []

    with open(dataset_path, 'r') as file:
        for line in file:
            line = line.strip()
            sentence_parts = line.split('\t')
            if len(sentence_parts) == 2:
                sentence_text, class_label = sentence_parts
                data.append((sentence_text, class_label))

    df: pd.DataFrame = pd.DataFrame(data, columns=['text', 'label'])

    # merge PUNCM, PUNCR, PUNC labels into PUNC:
    df['label'] = df['label'].replace(['PUNCM', 'PUNCR'], 'PUNC')
    # merge SPL and PART, as both relate to compound words. Rename to COMP
    df['label'] = df['label'].replace(['SPL', 'PART'], 'COMP')
    invalid_labels: List[str] = ['DER', 'X', 'FL']
    df = df[~df['label'].isin(invalid_labels)]

    return df
