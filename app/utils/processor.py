import PyPDF2
import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization")

def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def summarize_pdf(path):
    raw_text = extract_text_from_pdf(path)
    chunks = [raw_text[i:i+1000] for i in range(0, len(raw_text), 1000)]
    summaries = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

def generate_flashcards(summary):
    doc = nlp(summary)
    flashcards = []
    for sent in doc.sents:
        if '?' not in sent.text and len(sent.text.split()) > 6:
            keyword = [ent.text for ent in sent.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE']]
            if keyword:
                q = f"What is {keyword[0]}?"
                a = sent.text
                flashcards.append((q, a))
    return flashcards