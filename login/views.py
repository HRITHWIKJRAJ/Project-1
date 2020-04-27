from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import Customers
import urllib.request
import bs4 as bs
import tweepy
from textblob import TextBlob 

# Create your views here.
def page(request):
    return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request,'index.html')

def home(request):
    custs=Customers.objects.all()
    return render(request,"home.html",{'custs':custs})
def logout(request):
    auth.logout(request)
    return redirect('/')
def details(request, id):
    custids = Customers.objects.get(id=id)
    scrap_url = custids.link
    if custids.desc == "":
        source = urllib.request.urlopen(scrap_url).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        txt = ""
        for paragraph in soup.find_all('p'):
            block = str(paragraph.text)
            if block == None:
                pass
            else:
                txt +=  (str(paragraph.text))
        custids.desc = txt
        custids.save()
    return render(request,'details.html',{'custids':custids})

def chat(request):
    custs = Customers.objects.all()

    consumer_key = 'SI9QiqKHYNltMxWuFEMWotGIV'
    consumer_secret = 'QpBzbydvJC9wJpDzCRPDxSL4FiHmakC5rPTlu67flhr9XpLP9B'
    access_token = '1254320250205515777-kFSRUHhTQ1HYtRLGDy5nQFIT9Rqqb4'
    access_token_secret = 'MPFNqKVgYkjEtC3UvS0IpQM9KhzEqJPUBUXHQAtSZAX0m'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    for names in custs:
        polarity = 0
        subjectivity = 0
        name = str(names.name)
        public_tweets = api.search(name)

        for tweet in public_tweets:
            analysis = TextBlob(tweet.text)
            sentiment = analysis.sentiment
            polarity += sentiment.polarity
            subjectivity += sentiment.subjectivity
            names.pol = polarity
            names.sub = subjectivity
            names.save()
    
    return render(request,'chat.html',{'custs':custs})