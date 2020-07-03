from django.shortcuts import render
from django.http import HttpResponseRedirect
import random
from django.urls import reverse
import re
import markdown2
from . import util


def index(request):
    rand_list = [s for s in util.list_entries()]
    rand = random.choice(rand_list)
    return render(request, "encyclopedia/index.html", {
        "random": rand, "entries": util.list_entries()
    })

def title(request, title):
    rand_list = [s for s in util.list_entries()]
    rand = random.choice(rand_list)
    try:
        output= util.get_entry(title)
        entry = markdown2.markdown(output)
        return render(request, "encyclopedia/title.html", {
            "random": rand, "entry": entry , "title": title.capitalize(), "content": output
        })
    except FileNotFoundError:
        error = "No such file exists"
        return render(request, "encyclopedia/error.html", {
            "random": rand, "message": error
        }) 

def search(request):
    rand_list = [s for s in util.list_entries()]
    rand = random.choice(rand_list)
    if request.method == "POST":
        search = request.POST["q"]
        newlist = filter(lambda x: search in x, util.list_entries())
        if search in newlist:
            output= util.get_entry(search)
            entry = markdown2.markdown(output)
            return render(request, "encyclopedia/title.html", {
                "random": rand, "entry": entry , "title": search.capitalize(), "content": output
            })

        matching = [s for s in util.list_entries() if any(xs in s for xs in search)]
        return render(request, "encyclopedia/search.html", {
            "random": rand, "entries": matching , "search": True
        })
    return render(request, "encyclopedia/search.html", {
        "random": rand, "search": False
    })

def create(request):
    rand_list = [s for s in util.list_entries()]
    rand = random.choice(rand_list)
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title in util.list_entries():
            error = "Title already exists!"
            return render(request, "encyclopedia/error.html", {
                "random": rand, "message": error
            })
        new_entry = util.save_entry(title, content)
        output= util.get_entry(title)
        entry = markdown2.markdown(output)
        return render(request, "encyclopedia/title.html", {
            "random": rand, "entry": entry , "title": title.capitalize(), "content": output
        })
    return render(request, "encyclopedia/create.html", {
        "random": rand
    })

def edit(request):
    rand_list = [s for s in util.list_entries()]
    rand = random.choice(rand_list)
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        return render(request, "encyclopedia/edit.html", {
            "random": rand, "content": content, "title": title
        })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))

def update(request):
    rand_list = [s for s in util.list_entries()]
    rand = random.choice(rand_list)
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        new_entry = util.save_entry(title, content)
        output= util.get_entry(title)
        entry = markdown2.markdown(output)
        return render(request, "encyclopedia/title.html", {
            "random": rand, "entry": entry , "title": title.capitalize(), "content": output
        })
    return render(request, "encyclopedia/create.html", {
        "random": rand
    })