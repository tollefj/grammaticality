# POS-based grammaticality test
- Initially based on nearly ALL features from the UD conll structure
  - eventually reduced to merely using POS-tags and training on the sequences

### Pipeline:
1. Get UD file (train/test/dev)
2. Fetch sentences->tokens with `conllu` library
3. Extract features (for now, just POS) from the conll sentences
4. Get 95th percentile sentence length (for Norwegian UD train, this is `34`). Pad all sequences to length 34 with an `UNK` token
5. Map all POS-tags to integers to create a vector representation
6. Augment training data on a factor of 1:20 correct:incorrect sentences. This is a very naive approach, as the scrambling of POS-tags may produce correct grammars.
  - [ ] TODO: Perhaps we could use some CFGs to ensure ungrammaticality when generating nonsense.
  - Might need to tune the 1:20 factor/parameter, perhaps create 50 unique or even more, as there are certainly more combinations that are ungrammatical than not.
6. Train a BiLSTM on a binary label 1/0 
7. Predict and set a relatively low threshold for grammaticality (5% confidence). From limited testing, ungrammatical sentences usually have less than 1% confidence.

### Example output:
```c++
Nordmenn spiser for mye kjøtt
Original: ['NOUN', 'VERB', 'ADV', 'ADJ', 'NOUN']
--> Grammatical (51% confidence)
	Shuffled 0: ['NOUN', 'ADJ', 'ADV', 'VERB', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['ADJ', 'ADV', 'NOUN', 'VERB', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['ADJ', 'NOUN', 'VERB', 'NOUN', 'ADV']
	--> Ungrammatical (99% confidence)
____________________________________________________________
I kroppen vår har vi et hormon som heter insulin.
Original: ['ADP', 'NOUN', 'PRON', 'VERB', 'PRON', 'DET', 'NOUN', 'PRON', 'VERB', 'NOUN', 'PUNCT']
--> Grammatical (45% confidence)
	Shuffled 0: ['NOUN', 'PRON', 'PRON', 'DET', 'PUNCT', 'VERB', 'ADP', 'NOUN', 'NOUN', 'PRON', 'VERB']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['PRON', 'DET', 'NOUN', 'VERB', 'PUNCT', 'VERB', 'PRON', 'NOUN', 'NOUN', 'PRON', 'ADP']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['DET', 'VERB', 'PUNCT', 'NOUN', 'VERB', 'ADP', 'NOUN', 'PRON', 'PRON', 'PRON', 'NOUN']
	--> Ungrammatical (100% confidence)
Dette gjør oss i stand til å omdanne sukkeret vi spiser til energi.
Original: ['PRON', 'VERB', 'PRON', 'SCONJ', 'NOUN', 'SCONJ', 'PART', 'VERB', 'NOUN', 'PRON', 'VERB', 'ADP', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['PRON', 'VERB', 'ADP', 'NOUN', 'PUNCT', 'SCONJ', 'PART', 'PRON', 'NOUN', 'NOUN', 'VERB', 'VERB', 'PRON', 'SCONJ']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['VERB', 'VERB', 'PRON', 'PRON', 'PRON', 'SCONJ', 'NOUN', 'PART', 'ADP', 'NOUN', 'PUNCT', 'VERB', 'SCONJ', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['SCONJ', 'PRON', 'NOUN', 'PRON', 'VERB', 'PART', 'VERB', 'PUNCT', 'VERB', 'ADP', 'NOUN', 'PRON', 'SCONJ', 'NOUN']
	--> Ungrammatical (100% confidence)
Når man har diabetes type 2 virker ikke insulinet som det skal, og man får høyt blodsukker fordi mye av sukkeret blir værende i blodet.
Original: ['SCONJ', 'PRON', 'AUX', 'VERB', 'NOUN', 'NUM', 'VERB', 'PART', 'NOUN', 'PRON', 'PRON', 'VERB', 'PUNCT', 'CCONJ', 'PRON', 'VERB', 'ADJ', 'NOUN', 'SCONJ', 'ADJ', 'ADP', 'NOUN', 'VERB', 'ADJ', 'ADP', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['CCONJ', 'ADJ', 'NOUN', 'PUNCT', 'SCONJ', 'PRON', 'NOUN', 'NOUN', 'ADP', 'VERB', 'NOUN', 'NUM', 'SCONJ', 'VERB', 'VERB', 'PRON', 'ADJ', 'PART', 'VERB', 'NOUN', 'AUX', 'PRON', 'PRON', 'PUNCT', 'ADP', 'VERB', 'ADJ']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['VERB', 'NUM', 'SCONJ', 'VERB', 'SCONJ', 'PRON', 'VERB', 'NOUN', 'CCONJ', 'ADP', 'AUX', 'ADP', 'NOUN', 'ADJ', 'VERB', 'PUNCT', 'PRON', 'NOUN', 'VERB', 'PART', 'NOUN', 'NOUN', 'PRON', 'PRON', 'ADJ', 'PUNCT', 'ADJ']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['ADJ', 'ADP', 'VERB', 'PART', 'NUM', 'PUNCT', 'PRON', 'SCONJ', 'VERB', 'PRON', 'PUNCT', 'PRON', 'ADJ', 'PRON', 'ADP', 'SCONJ', 'NOUN', 'CCONJ', 'ADJ', 'VERB', 'VERB', 'NOUN', 'NOUN', 'NOUN', 'AUX', 'NOUN', 'VERB']
	--> Ungrammatical (100% confidence)
____________________________________________________________
Ifølge tall har omtrent 240.000 mennesker i Norge denne livsstilssykdommen.
Original: ['ADP', 'NOUN', 'VERB', 'ADV', 'NUM', 'NOUN', 'ADP', 'PROPN', 'DET', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['ADP', 'DET', 'ADP', 'NOUN', 'VERB', 'NOUN', 'PUNCT', 'ADV', 'NOUN', 'NUM', 'PROPN']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['ADV', 'ADP', 'ADP', 'NOUN', 'VERB', 'DET', 'PUNCT', 'NOUN', 'NOUN', 'NUM', 'PROPN']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['PUNCT', 'VERB', 'NUM', 'ADP', 'ADP', 'PROPN', 'DET', 'NOUN', 'NOUN', 'ADV', 'NOUN']
	--> Ungrammatical (100% confidence)
I tillegg regner man med at en del folk lever med sykdommen uten å være klar over det.
Original: ['ADP', 'NOUN', 'VERB', 'PRON', 'SCONJ', 'SCONJ', 'DET', 'NOUN', 'NOUN', 'VERB', 'ADP', 'NOUN', 'SCONJ', 'PART', 'AUX', 'ADJ', 'ADP', 'PRON', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['PRON', 'NOUN', 'SCONJ', 'NOUN', 'DET', 'PRON', 'NOUN', 'VERB', 'ADJ', 'ADP', 'ADP', 'NOUN', 'SCONJ', 'AUX', 'VERB', 'PART', 'PUNCT', 'ADP', 'SCONJ']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['DET', 'AUX', 'ADP', 'ADJ', 'VERB', 'NOUN', 'VERB', 'PUNCT', 'ADP', 'PRON', 'ADP', 'PRON', 'NOUN', 'NOUN', 'SCONJ', 'PART', 'NOUN', 'SCONJ', 'SCONJ']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['PRON', 'SCONJ', 'NOUN', 'ADP', 'ADP', 'NOUN', 'PRON', 'PART', 'VERB', 'SCONJ', 'DET', 'VERB', 'AUX', 'ADP', 'SCONJ', 'ADJ', 'PUNCT', 'NOUN', 'NOUN']
	--> Ungrammatical (100% confidence)
____________________________________________________________
I tillegg til dårlig kosthold kan overvekt, inaktivitet, røyking og alkohol utløse sykdommen.
Original: ['ADP', 'NOUN', 'ADP', 'ADJ', 'NOUN', 'AUX', 'NOUN', 'PUNCT', 'NOUN', 'PUNCT', 'NOUN', 'CCONJ', 'NOUN', 'VERB', 'NOUN', 'PUNCT']
--> Grammatical (71% confidence)
	Shuffled 0: ['ADP', 'NOUN', 'NOUN', 'ADJ', 'PUNCT', 'CCONJ', 'ADP', 'AUX', 'PUNCT', 'VERB', 'PUNCT', 'NOUN', 'NOUN', 'NOUN', 'NOUN', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['ADJ', 'NOUN', 'NOUN', 'AUX', 'NOUN', 'NOUN', 'NOUN', 'CCONJ', 'NOUN', 'PUNCT', 'VERB', 'NOUN', 'ADP', 'PUNCT', 'ADP', 'PUNCT']
	--> Ungrammatical (99% confidence)
	Shuffled 2: ['NOUN', 'NOUN', 'PUNCT', 'ADP', 'CCONJ', 'NOUN', 'AUX', 'PUNCT', 'ADP', 'VERB', 'NOUN', 'NOUN', 'NOUN', 'ADJ', 'NOUN', 'PUNCT']
	--> Ungrammatical (100% confidence)
Arv er også avgjørende.
Original: ['NOUN', 'AUX', 'ADV', 'ADJ', 'PUNCT']
--> Grammatical (67% confidence)
	Shuffled 0: ['AUX', 'ADJ', 'ADV', 'NOUN', 'PUNCT']
	--> Ungrammatical (98% confidence)
	Shuffled 1: ['ADV', 'AUX', 'ADJ', 'PUNCT', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['AUX', 'ADV', 'PUNCT', 'ADJ', 'NOUN']
	--> Ungrammatical (100% confidence)
Har du mor eller far med diabetes type 2, har du selv omtrent 40 prosent sjanse for å utvikle sykdommen i løpet av livet.
Original: ['VERB', 'PRON', 'NOUN', 'CCONJ', 'NOUN', 'ADP', 'PROPN', 'NOUN', 'NUM', 'PUNCT', 'VERB', 'PRON', 'DET', 'ADV', 'NUM', 'NOUN', 'NOUN', 'SCONJ', 'PART', 'VERB', 'NOUN', 'ADP', 'NOUN', 'ADP', 'NOUN', 'PUNCT']
--> Grammatical (78% confidence)
	Shuffled 0: ['NOUN', 'PRON', 'NOUN', 'VERB', 'PART', 'NOUN', 'ADP', 'ADP', 'VERB', 'PROPN', 'PUNCT', 'NOUN', 'DET', 'SCONJ', 'PUNCT', 'NOUN', 'NOUN', 'PRON', 'NOUN', 'VERB', 'NOUN', 'ADP', 'CCONJ', 'NUM', 'ADV', 'NUM']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['NOUN', 'VERB', 'NOUN', 'PART', 'PUNCT', 'NOUN', 'NOUN', 'VERB', 'NUM', 'ADP', 'NUM', 'NOUN', 'NOUN', 'PRON', 'CCONJ', 'ADV', 'PROPN', 'PUNCT', 'DET', 'ADP', 'SCONJ', 'ADP', 'NOUN', 'NOUN', 'VERB', 'PRON']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['NOUN', 'CCONJ', 'NUM', 'PRON', 'VERB', 'PRON', 'VERB', 'VERB', 'PUNCT', 'DET', 'NUM', 'PART', 'NOUN', 'NOUN', 'ADP', 'NOUN', 'NOUN', 'PROPN', 'PUNCT', 'SCONJ', 'ADV', 'ADP', 'NOUN', 'NOUN', 'ADP', 'NOUN']
	--> Ungrammatical (100% confidence)
____________________________________________________________
Resultatene fra den nye studien viser at man i Norge i 1990 estimerte at 64,9 prosent av tilfellene av sykdommen skyldtes dårlig kosthold.
Original: ['NOUN', 'ADP', 'DET', 'ADJ', 'NOUN', 'VERB', 'SCONJ', 'PRON', 'ADP', 'PROPN', 'ADP', 'NUM', 'VERB', 'SCONJ', 'NUM', 'NOUN', 'ADP', 'NOUN', 'ADP', 'NOUN', 'VERB', 'ADJ', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['NOUN', 'ADJ', 'VERB', 'NOUN', 'ADP', 'NOUN', 'PRON', 'PROPN', 'ADP', 'NOUN', 'VERB', 'SCONJ', 'ADP', 'NUM', 'ADJ', 'NUM', 'SCONJ', 'ADP', 'NOUN', 'DET', 'VERB', 'PUNCT', 'ADP', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['DET', 'ADP', 'ADP', 'NOUN', 'VERB', 'NOUN', 'SCONJ', 'SCONJ', 'VERB', 'ADP', 'PUNCT', 'NOUN', 'ADJ', 'VERB', 'ADJ', 'NOUN', 'ADP', 'NUM', 'NUM', 'PRON', 'NOUN', 'NOUN', 'ADP', 'PROPN']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['ADP', 'NOUN', 'ADP', 'PUNCT', 'ADJ', 'ADJ', 'NUM', 'NOUN', 'PROPN', 'DET', 'VERB', 'NUM', 'NOUN', 'SCONJ', 'ADP', 'PRON', 'NOUN', 'ADP', 'NOUN', 'ADP', 'VERB', 'NOUN', 'VERB', 'SCONJ']
	--> Ungrammatical (100% confidence)
I 2018 hadde dette tallet steget til 75,1 prosent.
Original: ['ADP', 'NUM', 'AUX', 'DET', 'NOUN', 'VERB', 'ADP', 'NUM', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['ADP', 'NUM', 'NUM', 'PUNCT', 'AUX', 'DET', 'NOUN', 'ADP', 'VERB', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['NOUN', 'ADP', 'AUX', 'ADP', 'DET', 'NUM', 'NUM', 'NOUN', 'PUNCT', 'VERB']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['NOUN', 'NOUN', 'ADP', 'ADP', 'PUNCT', 'DET', 'NUM', 'VERB', 'AUX', 'NUM']
	--> Ungrammatical (100% confidence)
____________________________________________________________
Og grunnen til dette?
Original: ['CCONJ', 'NOUN', 'ADP', 'PRON', 'PUNCT']
--> Grammatical (17% confidence)
	Shuffled 0: ['PRON', 'ADP', 'CCONJ', 'NOUN', 'PUNCT']
	--> Ungrammatical (99% confidence)
	Shuffled 1: ['PUNCT', 'ADP', 'CCONJ', 'NOUN', 'PRON']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['CCONJ', 'ADP', 'PUNCT', 'PRON', 'NOUN']
	--> Ungrammatical (100% confidence)
Vi spiser for mye rødt og bearbeidet kjøtt, mener forskerne.
Original: ['PRON', 'VERB', 'ADV', 'ADJ', 'ADJ', 'CCONJ', 'ADJ', 'NOUN', 'PUNCT', 'VERB', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['ADV', 'VERB', 'CCONJ', 'ADJ', 'PRON', 'VERB', 'PUNCT', 'NOUN', 'PUNCT', 'NOUN', 'ADJ', 'ADJ']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['ADJ', 'VERB', 'PRON', 'ADJ', 'ADJ', 'ADV', 'NOUN', 'PUNCT', 'NOUN', 'VERB', 'CCONJ', 'PUNCT']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['CCONJ', 'VERB', 'ADJ', 'ADV', 'PRON', 'PUNCT', 'NOUN', 'VERB', 'PUNCT', 'NOUN', 'ADJ', 'ADJ']
	--> Ungrammatical (100% confidence)
I tillegg har vi nordmenn et utilstrekkelig inntak av fullkorn.
Original: ['ADP', 'NOUN', 'VERB', 'PRON', 'NOUN', 'DET', 'ADJ', 'NOUN', 'ADP', 'NOUN', 'PUNCT']
--> Grammatical (83% confidence)
	Shuffled 0: ['NOUN', 'PRON', 'ADP', 'VERB', 'NOUN', 'PUNCT', 'NOUN', 'DET', 'ADJ', 'NOUN', 'ADP']
	--> Ungrammatical (100% confidence)
	Shuffled 1: ['PRON', 'ADP', 'NOUN', 'PUNCT', 'ADJ', 'NOUN', 'DET', 'VERB', 'ADP', 'NOUN', 'NOUN']
	--> Ungrammatical (100% confidence)
	Shuffled 2: ['ADJ', 'VERB', 'NOUN', 'ADP', 'PRON', 'DET', 'NOUN', 'PUNCT', 'ADP', 'NOUN', 'NOUN']
	--> Ungrammatical (100% confidence)
____________________________________________________________

```