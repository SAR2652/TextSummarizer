from django.shortcuts import render
from django.contrib import messages


import re, heapq
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
# Create your views here.

def extractive_summarize(text):
    # Text preprocessing
    text = re.sub(r'\[[0-9]*\]', ' ', text)  # remove numeric citations
    text = re.sub(r'\s+', ' ', text)  # remove 1+ continuous whitespaces
    clean_text = text.lower()  # convert all text to lower case
    clean_text = re.sub(r'\W', ' ', clean_text)  # remove non-word characters
    # clean_text = re.sub(r'\d', ' ', clean_text)  # remove any digits
    # remove 1+ continuous whitespaces
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Tokenization
    sentences = sent_tokenize(text)
    stop_words = stopwords.words('english')

    # Initialize an empty dictionary to store the count of words
    word2count = {}
    for word in word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():  # create new key as word
                word2count[word] = 1
            else:
                word2count[word] += 1

    # standardize all values
    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())

    # Generate a dictionary of sentence scores
    sent2score = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 30:   # sentence length condition
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

    best_sentences = heapq.nlargest(5, sent2score, key=sent2score.get)
    return best_sentences


def summarize(request):
    output_dict = dict()
    if request.method == 'POST':
        text = request.POST.get('text')
        if len(sent_tokenize(text)) > 5:
            sentences = extractive_summarize(text)
            output_dict['text'] = text
            output_dict['summary'] = sentences
            output_dict['alert_flag'] = False
            return render(request, 'summary.html', output_dict)
        else:
            output_dict['alert_flag'] = True
            return render(request, 'Summarizer/summarizer.html', output_dict)
    else:
        return render(request, 'Summarizer/summarizer.html', output_dict)

        
