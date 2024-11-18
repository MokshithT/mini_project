import re
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import heapq

nltk.download('punkt')
nltk.download('stopwords')

# Load SpaCy model
nlp = spacy.load('en_core_web_lg')

# NLTK Summarizer
def nltk_summarizer(docx):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(docx)
    freqTable = {}
    for word in words:
        word = word.lower()
        if word not in stopWords:
            freqTable[word] = freqTable.get(word, 0) + 1

    sentence_list = sent_tokenize(docx)
    max_freq = max(freqTable.values()) if freqTable else 0
    for word in freqTable:
        freqTable[word] = freqTable[word] / max_freq if max_freq > 0 else 0

    sentence_scores = {}
    for sent in sentence_list:
        for word in word_tokenize(sent.lower()):
            if word in freqTable and len(sent.split(' ')) < 30:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freqTable[word]

    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

# SpaCy Summarizer
def spacy_summarizer(docx):
    doc = nlp(docx)
    stopWords = list(STOP_WORDS)
    freqTable = {}
    for word in doc:
        if word.text.lower() not in stopWords and word.is_alpha:
            freqTable[word.text.lower()] = freqTable.get(word.text.lower(), 0) + 1

    max_freq = max(freqTable.values()) if freqTable else 0
    for word in freqTable:
        freqTable[word] = freqTable[word] / max_freq if max_freq > 0 else 0

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in freqTable and len(sent.text.split(' ')) < 30:
                sentence_scores[sent.text] = sentence_scores.get(sent.text, 0) + freqTable[word.text.lower()]

    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def contributors_page():
    st.title("Text Summurization using NLP")
    st.subheader("Abstract")
    st.write("The project aims to create an automated Text Summarization system using Natural Language Processing (NLP) techniques to condense large text volumes into concise summaries. SpaCy, a powerful NLP library, is used to process text data by identifying and removing stop words, tokenizing, and calculating word frequencies. The system uses an extractive summarization method, selecting sentences with the highest importance scores based on word frequencies. The input text is processed to identify the most frequently occurring words, normalize word frequencies, and score each sentence based on their frequency. The top 30% of sentences with the highest scores are selected for a concise summary. The Streamlit web application allows users to input text and retrieve the summary instantly, making it useful for tasks like information retrieval, content generation, and knowledge management.")
    st.write("year of contibution: 2024")
    st.title("Contributors & Guidance")
    st.write("1. **Mokshith Thota** [LinkedIn](https://www.linkedin.com/in/mokshith16/)")
    st.write("2. **Chandu Ummanaveni** [LinkedIn](https://www.linkedin.com/in/chandu-ummanaveni-592822255/)")
    st.write("3. **Tharun Gadidas** [LinkedIn](https://www.linkedin.com/in/tharun-gadidasu-173658257/)")
        

    st.subheader("Guidance")
    st.write("**Mr. Ch. Naveen Kumar**")
    st.write("Assistant Professor  at Emerging Technologies (MRCET)")

import pyperclip  # Make sure to install this package

def main():
    st.sidebar.title("Navigation")
    options = ["Summarize Text", "Contributors"]
    choice = st.sidebar.selectbox("Select Page", options)

    if choice == "Summarize Text":
        st.title("Text Summarizer App")
        st.subheader("Summary using NLP (SpaCy)")
        article_text = st.text_area("Enter Text Here")

        # Cleaning of input text
        article_text = re.sub(r'\\[[0-9]*\\]', ' ', article_text)
        article_text = re.sub('[^a-zA-Z.,]', ' ', article_text)
        article_text = re.sub(r"\b[a-zA-Z]\b", '', article_text)
        article_text = re.sub("[A-Z]\Z", '', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        if st.button("Summarize Text"):
            if not article_text.strip():
                st.warning("Please enter some text to summarize.")
            elif len(article_text.split()) < 20:  # Check for minimum length (e.g., 20 words)
                st.warning("Please provide more information to summarize correctly.")
            else:
                summary_result = spacy_summarizer(article_text)
                st.write(summary_result)
                
    elif choice == "Contributors":
        contributors_page()

if __name__ == '__main__':
    main()
