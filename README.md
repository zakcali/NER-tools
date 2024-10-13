# NER-tools

To facilitate NER data manipulation, we created the NER-tools GitHub repository, featuring useful scripts. Here is the scripts and their usage:

•	jsonl2html.py converts a file created by doccano into a visual HTML file.

•	jsonl2spacy.py converts a file created by doccano into a spacy-json file.

•	docbin2jsonl.py converts a file named dev.spacy into a doccano format file named dev.jsonl.

•	spacy2docbin.py converts a spacy-json file into a spacy-docbin file.

•	spacysplit2docbin.py converts a spacy-json file into spacy-docbin files named train.spacy and dev.spacy

•	html2jsonl.py converts a visual HTML file into a doccano jsonl file.

•	combine-htmls.py combines multiple HTML files into a single html file.

•	spacy-f1cm.py given that a trained model (model-best) and spacy test json file (test.json) in the same folder, creates confusion_matrix.png, confusion_matrix_report.txt, and entity_recognition_report.txt

To convert html to spacy docbin format, one must run scripts sequentially html2jsonl.py -> jsonl2spacyjson.py -> spacy2docbin.py

•	bio_converter.py splits and converts entities_f1.csv file into y_pred.bio and y_true.bio

•	seqevalF1.py reads y_pred.bio and y_true.bio and calculates metrics with python seqeval library.

•	patch-to-scorer.py: patched get_ner_prf function of scorer.py of spaCy V3.7.5 in directory C:\Python\Python311\Lib\site-packages\spacy to output more metrics.


nodejs folder
requirements: prompt.html file in the same folder, reports folder holds radiology reports in text format (endfing with .txt extension), empty outputs folder, google generative-ai api installed in node_modules folder
scripts read prompt.html from current folder, read reports from reports folder, outputs tagged reports to outputs folder

•	test-bt-orig.js : test script run on April 2024 with gemini 1.5 pro preview api with 1 million tokens context length

•	test-bt-exp-0827.js :  test script run now (on Oct) 2024 with gemini 1.5 pro experimental 0827 api with 2 million tokens context length



