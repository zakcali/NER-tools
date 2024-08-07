import spacy
import sys
import ast
from spacy.tokens import DocBin
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex, compile_suffix_regex, compile_prefix_regex


def convert_json(source_file, destination_file):
    nlp = spacy.blank("tr")
    # Define your specific characters for isolation
    special_chars = r"-();,.\n"

    # Modified infix pattern for precise isolation
    infixes = [
        rf"(?<=[^0-9,.])[{special_chars}](?=[^0-9,.])",  # Special character not between digits or periods/commas
        rf"(?<=[^0-9{special_chars}])(?=[{special_chars}])",
        # Before any special character, not preceded by digit or special char
        rf"(?<=[{special_chars}])(?=[^0-9{special_chars}])",
        # After any special character, not followed by digit or special char
        r"(?<=\d)(?=[\(\)\[\]{{\}}])",  # Split between digit and opening/closing brackets or parentheses
        r"(?<=[\(\)\[\]{{\}}])(?=\d)",  # Split between opening/closing brackets or parentheses and digit
        r"(?<=\w)(?=[\(\)\[\]{{\}}])",  # Split between word character and opening/closing brackets or parentheses
        r"(?<=[\(\)\[\]{{\}}])(?=\w)",  # Split between opening/closing brackets or parentheses and word character
        r"(?<=\w)(?=[;])",  # Split between word character and semicolon
        r"(?<=[;])(?=\d)",  # Split between semicolon and digit
    ]

    # Define suffixes to split punctuation at the end of words
    suffixes = [
        r"(?<=[a-zA-Z])\.",  # Period after letters
        r"(?<=[a-zA-Z]);",  # Semicolon after letters
        r"\.$",  # Period at the end of a token
        r";$",  # Semicolon at the end of a token
        r"\n$"  # Newline at the end of a token
    ]

    # Define prefixes to split punctuation at the beginning of words
    prefixes = [
        r"^[({\[]",  # Parentheses, braces, and brackets at the beginning
        r"^[.,;:-]"  # Punctuation at the beginning
    ]

    # Compile the infix, suffix, and prefix patterns
    infix_re = compile_infix_regex(infixes)
    suffix_re = compile_suffix_regex(suffixes)
    prefix_re = compile_prefix_regex(prefixes)

    def custom_tokenizer(nlp):
        return Tokenizer(nlp.vocab, prefix_search=prefix_re.search, infix_finditer=infix_re.finditer,
                         suffix_search=suffix_re.search, token_match=None)

    nlp.tokenizer = custom_tokenizer(nlp)

    # the DocBin will store the example documents
    db = DocBin()

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
        training_data = ast.literal_eval(content)  # Safely evaluate the file content as a Python literal

    for text, annotations in training_data:
        doc = nlp(text)
        for token in doc:
            print(token.idx, token.text, token.whitespace_)
        ents = []
        # Access the 'entities' list from the annotations dictionary
        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            print(f"start: {start}, end: {end}, span: {span}")
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(destination_file)


arguments = sys.argv
if len(arguments) > 1:
    print("Converting spacy json file, named:", arguments[1], "into spacy docbin file")
    convert_json(arguments[1] + ".json", arguments[1] + ".spacy")
else:
    print("Converting spacy json file, named input.json into spacy docbin file, named train.spacy")
    convert_json('input.json', 'train.spacy')
