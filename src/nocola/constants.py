error_mapping = {
    "F": "Wrong morpho-syntactic form",
    "INFL": "Suffix from correct category, but the wrong form",
    "W": "Wrong word",
    "ORT": "Wrong spelling of word",
    "M": "Word should be added",
    "R": "Word should be removed",
    "PUNC": "Add or remove punctuation",
    "PUNCM": "Punctuation mark should be added",
    "PUNCR": "Punctuation mark should be removed",
    "O": "Wrong word order",
    "CAP": "Add or remove capitalization",
    "PART": "Compounding error",
    "SPL": "Compounding missing",
    "DER": "Derivation",
}

label_mapping = {
    "F": 0,
    "INFL": 1,
    "W": 2,
    "ORT": 3,
    "M": 4,
    "R": 5,
    "PUNC": 6,
    "PUNCM": 7,
    "PUNCR": 8,
    "O": 9,
    "CAP": 10,
    "PART": 11,
    "SPL": 12,
    "DER": 13, 
}

label_decoding = {v:k for k,v in label_mapping.items()}