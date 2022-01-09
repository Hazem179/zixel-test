import spacy
import spacy_ke

# load spacy model
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("yake")


def tags_extraction(description):
    tags = []
    doc = nlp(description)
    for keyword, score in doc._.extract_keywords(n=10):
        tags.append(str(keyword))
        print(keyword,score)
    return tags