from django.shortcuts import render

from . models import ScenePage

def index(request, scenename):
    print(scenename)
    pg = ScenePage.objects.get(slug=scenename)

    context = {
        'title': pg.title,
        'author': pg.author,
        'date_published': pg.date_published,
    }
    #assert False #to test debugger
    #helper function from Django
    return render(request, 'architettura/scene_page.html', context)
