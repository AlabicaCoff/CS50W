from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from random import randint

from . import util

from markdown2 import Markdown

def convert_md_to_html(filename):
    content = util.get_entry(filename)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This title does not exist. Please try again."
            }
        )
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
            }
        )

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title in util.list_entries():
            return render(request,"encyclopedia/error.html", {
                "message": "This title does already exist. Please try again."
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
            }
        )

def random(request):
    entries=util.list_entries()
    return redirect("entry", title=entries[randint(0, len(entries)-1)])

def search(request):
    q = request.POST.get('q')
    if q in util.list_entries():
        return redirect("entry", title=q)
    else:
        results = []
        for entry in util.list_entries():
            if q in entry:
                results.append(entry)
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "Your search is not found. Please try again."
                    }
                )
        return render(request, "encyclopedia/search.html", {
            "results": results
            }
        )