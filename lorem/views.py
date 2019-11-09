from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from gensim.models.keyedvectors import KeyedVectors
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE, "GoogleNews-vectors-negative300.bin")
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

def home(request):

    from utils.DocSim import DocSim
    ds = DocSim(w2v_model)

    source_doc = ""
    if(request.method == "POST"):
        query = request.POST['myQuery']
        source_doc = query

    # Calling Daily Star Rss
    from utils.DailyStarRss import DailyStarRss
    DailyRss()
    
    dstar = open(os.path.join(BASE, "dailyStar_top_news.txt"), "r")
    lines = dstar.readlines()
    target_docs = []
    for line in lines:
        target_docs.append(line)

    # Calling Al Jazeera Rss
    from utils.alJazeeraRss import alJazeeraRss
    AlRss()
    
    dstar = open(os.path.join(BASE, "aljazeera_news.txt"), "r")
    lines = dstar.readlines()

    for line in lines:
        target_docs.append(line)


    # Calling NYTimes Rss
    from utils.nytimesrss import nytimesrss
    NyRss()
    
    dstar = open(os.path.join(BASE, "nytimes_news.txt"), "r")
    lines = dstar.readlines()
    
    for line in lines:
        target_docs.append(line)


    # Calling theGuardian Rss
    from utils.theGuardian import theGuardian
    GuRss()
    
    dstar = open(os.path.join(BASE, "guardian_news.txt"), "r")
    lines = dstar.readlines()
    
    for line in lines:
        target_docs.append(line)

    # print(source_doc)

    sim_scores = ds.calculate_similarity(source_doc, target_docs)

    acc = 0
    for i in range(len(sim_scores)):
        score = sim_scores[i]['score']
        doc = sim_scores[i]['doc']
        
        if acc < score:
            acc = score

    result = round(acc*100, 1)
    # print(result)

    outputs = [
        {
            'queryString': source_doc,
            'resultString': str(result)
        }
    ]

    context = {
        'outputs': outputs
    }

    return render(request, 'lorem/home.html', context)

def about(request):
    return render(request, 'lorem/about.html', {'title': 'About'})
