from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util
"""
Variables
==============================================================================================================
1. title is global varaible used to store the search query passed from the form in layout.html
2. new_title is global variable used to store the title of new data to be added passed from create.html
3. new_desc is global variable used to store the description of new data to be added passed from create.html
==============================================================================================================
Functions
==============================================================================================================
1. index function is used to display all the data that exists in entries folder as .md file.
2. search function is used to search the wiki page for existing data.
3. create function is used to visit the form page for entrering new data.
4. save function is used to save the files as .md files with title as file name and description as the data in the .md file
"""
title = ""
new_title = ""
new_desc = ""

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    mark = markdown2.Markdown()
    if request.method == "POST":
        title = request.POST.get("q")
    else:
        return HttpResponse("Resubmit form!")
    return render(request, "encyclopedia/get.html", {
        "data": mark.convert(util.get_entry(title)), "header": title
    })

def create(request):
    return render(request, "encyclopedia/create.html")

def save(request):
    if request.method == "POST":
        new_title = request.POST.get("t")
        new_desc = request.POST.get("d")
    else:
        return render(request, "encyclopedia/error.html")
    return HttpResponseRedirect(reverse('index'))

def wiki(request, query):
    mark = markdown2.Markdown()
    return render(request, "encyclopedia/wiki.html", {
        "data": mark.convert(util.get_entry(query)),
        "title": query
    })

def edit(request, title):
    return render(request, "encyclopedia/edit.html", {
        "data": util.get_entry(title),
        "title": title
    })

def save_edit(request, title):
    if request.method == "POST":
        data = request.POST["e"]
    return render(request, "encyclopedia/index.html", {
        "updated_data": util.save_entry(title, data)
    })
