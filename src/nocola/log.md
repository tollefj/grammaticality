# Thursday, Jun 1.

"**Jeg har ikke lenger lyst å jobbe** første året som **au-pair, vaskehjelp, butikkmedarbeider etc**, for å _ha bedre sjanse til å_ få en bedre jobb _etterpå_"


au-pair, vaskehjelp, butikkmedarbeider  -> "concept of cleaning/helping" -> enkle arbeidsoppgaver

Evaluation types:
- LLM probability of a sentence (ps1, ps2)
	- train on word-order prob, sentence prob,...
	- prob based on the error types (R, M, PUNCT, ...)

	- Modeling:
		- NBBERT
			- jobbe første året som au-pair
				- [MASK] første året som au-pair
				- jobbe [MASK] ...
				- jobbe første året som [MASK]
					prob(MASK) = 0.8
- Regression problem on grammaticality (probably difficult)
	- jobbe første år som au-pair -> 0.7
	- jobbe første året au-pair -> 0
	- Da gikk hun i niene klassen -> 0.9 (SPL)
	- Da gikk hun i niendeklassen -> 1.0

	- Possibility:
		- which words can be combined
 
- Unsupervised approach:
	- use NCC (norw. colossal corp)
		- do mutations (actions: replace/swap/delete) to create a parallel dataset
			- train on the errors
	- pros: more data
	- cons: no proper evaluation
		- user testing, empirical eval

## What is the goal:
- SCRIBE-MEGAS
	- TV subtitles: verbatim subtitles are long, people can't read them
		- needs to be compressed
			- deaf/h-o-h don't care about the actual grammaticality
				- they want something that works!!!
	- Headlines
	- Interviews, live transcription
	- Bullet points for something (article, ++)





# Friday, May 12.
**Ole J:**
After reading the paper, I think have come up with a simpler (idea for) fitness function, or functions,  to evaluate two sentences s_1 and s_2.

In our case, one sentence - say s_1 - would be the original sentence while the other sentence - s_2 - would be the compressed sentence.

I suggest to use NoCoLA_zero model., which computes p(s_1) and p(s_2).
Here, p(s_i) is the probability of acceptability, based on the LLM's "innate grammatical understanding" as they say.

Thus, typically p(s_1) would be "high"
p(s_2) would be "low"
with p(s_1) > p(s_2)

We could use as fitness f(s_1,s_2) =  p(s_1) - p(s_2) and try to minimize it, the idea being the closer s_2 is to s_1, the better it is in terms of language acceptability.

But to be more general and have a lower bound on fitness we may instead want to use
f(s_1,s_2) =  abs(p(s_1) - p(s_2))
or
f(s_1,s_2) =  (p(s_1) - p(s_2))^2, and still minimize.

___

**svar:**
I agree with your observations of the evaluation - which aligns with the comments of some reviewers as well.

I like the idea of comparing probabilities here, but I think we need to remember the following:
- the model will merely do an action: permutation/swap/delete
	- it will not create magical misspellings (i.e. that of a foreigner writing Norwegian, which this dataset is based on)

so what are we actually learning to minimize here?
It may deviate from the goals of finding the most probable sentence based on the above actions taken in the selection process?
I can run some experiments with NBBERT, as they stated gave superior results. I can also apply this with sentence-bert with the same foundation model, which is trained using siamese BERT-nets.

I also want to cross-check the grammaticality here with the simpler model I built earlier on!



I did a test-run (finished tonight) on the class-dataset using sentence-bert: https://huggingface.co/tollefj/setfit-nocola-20-iter-25-epochs-allsamples, to predict which error a sentence belongs to, out of the 14 classes. I assume this will have quite low accuracy, but haven't checked yet!
- Xavier and I thought that we might be able to use the classification as some numbering scheme (i.e. importance score)
	- But this requires pretty solid accuracy for the system to work well.

# 11 mai, 14:25
Har satt opp NoCoLa datasettet, omformet det litt, og begynt å jobbe med datainspeksjon.
Spurt chatgpt om å definere viktigheten av hver kategori:

- Wrong word order (O): Incorrect word order can significantly impact the meaning and clarity of a sentence, making it the most crucial error to address.
- Wrong morpho-syntactic form (F) and Suffix from correct category - wrong form for this word (INFL): These errors involve incorrect word forms and can affect grammaticality and meaning.
- Wrong word (W) and Wrong spelling of word (ORT): These errors can introduce ambiguity or convey a different meaning, impacting the overall clarity and precision of the text.
- Word should be added (M) and Word should be removed (R): Superfluous or missing words can affect sentence structure and coherence, but they may not necessarily result in significant comprehension issues.
- Add or remove punctuation (PUNC, PUNCM, PUNCR): Punctuation errors can impact the flow and interpretation of a sentence, but their impact may be relatively minor compared to other errors.
- Add or remove capitalization (CAP): Capitalization errors generally have a minor impact on understanding, as they primarily affect stylistic conventions and emphasis.
- Compounding (PART, SPL): Deviations in compounding may introduce errors, but their significance depends on the specific words involved and the syntactic structure.
- Derivation (DER): Deviations in word derivation may affect the precision of the language but might have a relatively lower impact on overall comprehension.


## Vi har også muligheten for parallel-trening med `zero`datasettet:
- Split the dataset: Divide the preprocessed dataset into training, validation, and test sets. A typical split ratio might be 80% for training, 10% for validation, and 10% for testing.
- Choose a model architecture: Select a suitable model architecture for the task, such as a sequence-to-sequence model with attention, a Transformer-based model, or another advanced model that's well-suited for text generation tasks.
- Fine-tune the model: Train the model on the training set using the erroneous sentences as input and their corrected counterparts as the target output. Monitor the model's performance on the validation set during training to avoid overfitting and choose the best-performing model.
- Evaluate the model: Test the trained model's performance on the test set. Use appropriate evaluation metrics like BLEU, ROUGE, or other relevant metrics that measure the quality of the generated sentences compared to the corrected ground truth sentences.
- Post-process and analyze: After generating the corrected sentences, you can perform post-processing steps, if necessary, to ensure proper formatting, capitalization, or other desired characteristics. Analyze the model's performance and identify any common error patterns that it might struggle with, which can help inform future improvements to the model.
- Iterate and improve: Based on the evaluation results and analysis, improve the model by fine-tuning the architecture, adjusting the training process, or augmenting the dataset with more examples or different error types.

Once you have a well-performing sentence rewriting model, you can use it to correct errors in sentences while preserving their original meaning, making it a valuable tool for language learners, educators, and content creators

## Other suggestions:

- Error Detection and Correction: Train a model to identify and correct errors in sentences by comparing the erroneous and corrected versions. This would involve detecting the type of error (W, M, F, or ORT) and making appropriate corrections. In this case, the model could predict the difficulty of a sentence based on the type and number of errors present.
- Error Analysis: Develop a model to analyze and classify the types of errors (W, M, F, or ORT) present in a given text. This could help understand the most common types of errors and aid in the development of targeted teaching or learning materials.
- Sentence Rewriting: Train a model to rewrite sentences with errors in a way that maintains the original meaning but corrects the mistakes. This would involve understanding the context and making the necessary corrections while keeping the sentence coherent.
- Error-aware Machine Translation: Integrate error detection and correction into a machine translation model, allowing the model to automatically correct errors in the source text before translating it. This could improve the overall translation quality.
- Assessing Language Proficiency: Use the dataset to build a model that can assess a learner's language proficiency level by analyzing their writing and identifying the types and frequency of errors they make. This could help tailor language instruction to a learner's specific needs.
- Generating Targeted Practice Exercises: Create a model that can generate targeted practice exercises based on the types of errors a learner commonly makes, allowing them to focus on improving specific areas of their language skills.