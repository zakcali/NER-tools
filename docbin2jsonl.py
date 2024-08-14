import spacy
from spacy.tokens import DocBin
import srsly

path_data = "dev.spacy"

nlp = spacy.blank("en")

doc_bin = DocBin().from_disk(path_data)
examples = []
i=0

for doc in doc_bin.get_docs(nlp.vocab):
    i+=1
    spans = [[ent.start_char,ent.end_char,ent.label_] for ent in doc.ents]
    comments = []
    examples.append({"id": i, "text": doc.text, "label": spans, "Comments": comments})

srsly.write_jsonl("dev.jsonl", examples)