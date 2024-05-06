from django.shortcuts import render
from markdown import Markdown
from . import util
import random 

def mdconverter(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    htmlcontent = mdconverter(title)
    if htmlcontent is None:
        return render(request, "encyclopedia/errorpage.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entrypage.html", {
            "title": title,
            "content": htmlcontent
        })

def search(request):
    if request.method == "POST":
        entrysearch = request.POST['q']
        htmlcontent = mdconverter(entrysearch)
        if htmlcontent is not None:
            return render(request, "encyclopedia/entrypage.html" , {
                "title": entrysearch,
                "content": htmlcontent
            })
        else:
            alltheEntries = util.list_entries()
            recommendations = []
            for entry in alltheEntries:
                if entrysearch.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/searchpage.html", {
                "recommendation": recommendations 
            })

def newentry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/errorpage.html", {
                "message": "Entry Page Already Exists"
            })
        else:
            util.save_entry(title, content)
            htmlcontent = mdconverter(title)
            return render(request, "encyclopedia/newentry.html", {
                "title": title,
                "content": htmlcontent
            })
        
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
        })


def saveedit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        htmlcontent = mdconverter(title)
        return render(request, "encyclopedia/entrypage.html", {
            "title": title,
            "content": htmlcontent
        })

def randomchoice(request):
    allTheEntries = util.list_entries()
    randomentry = random.choice(allTheEntries)
    htmlcontent = mdconverter(randomentry)
    return render(request, "encyclopedia/entrypage.html", {
        "title": randomentry,
        "content": htmlcontent
    })