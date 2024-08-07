# NER-tools

To facilitate NER data manipulation, we created the NER-tools GitHub repository (https://github.com/zakcali/NER-tools ), featuring useful scripts like jsonl2html.py, jsonl2spacy.py, and many more. Here is the scripts and their usage:

•	jsonl2html.py converts a file created by doccano into a visual HTML file.

•	jsonl2spacy.py converts a file created by doccano into a spacy-json file.

•	spacy2docbin.py converts a spacy-json file into a spacy-docbin file.

•	spacysplit2docbin.py converts a spacy-json file into spacy-docbin files named train.spacy and dev.spacy

•	html2jsonl.py converts a visual HTML file into a doccano jsonl file.


To convert html to spacy docbin format, one must run scripts sequentially html2jsonl.py -> jsonl2spacyjson.py -> spacy2docbin.py
