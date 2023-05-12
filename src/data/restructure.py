import os

splits = ['train', 'dev', 'test']
path = "nocola/datasets"
_id = "NoCoLa_class_"
new_id = "nocola_parsed/nocola_"
os.makedirs("nocola_parsed", exist_ok=True)

for split in splits:
    fp = os.path.join(path, f"{_id}{split}.txt")
    gram_f = f"{new_id}grammatical_{split}.txt"
    ungram_f = f"{new_id}ungrammatical_{split}.txt"
    with open(fp, "r", encoding="utf-8") as input_file, \
         open(gram_f, 'w', encoding="utf-8") as grammatical_file, \
         open(ungram_f, 'w', encoding="utf-8") as ungrammatical_file:

        output_files = [None, ungrammatical_file, grammatical_file]

        for line in input_file:
            if line.startswith("Ungrammatical:"):
                output_index = 1
            elif line.startswith("Grammatical:"):
                output_index = 2
            elif line.strip():
                output_files[output_index].write(line.strip() + '\n')

            