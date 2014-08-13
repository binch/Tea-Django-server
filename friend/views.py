# Create your views here.

from friend.models import *

def get_articles(request):
    articles = Document.objects.all()
    for article in articles:
        print article.text
    return
    
