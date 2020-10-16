from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
from django import forms
from django.http import HttpResponse

import random

import re

from markdown2 import Markdown

class NewTitle(forms.Form):
    title = forms.CharField(label="New title")
    content = forms.CharField(label="", widget = forms.Textarea(attrs={
        "placeholder": "Enter the Markdown content for the title"
    }))

class updateTitle(forms.Form):
    newContent = forms.CharField(label="", widget=forms.Textarea(attrs={
        "autofocus": "autofocus"
    }))

def index(request):     
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if entry:
        markdowner = Markdown()
        content = markdowner.convert(entry)
        with open("encyclopedia/templates/encyclopedia/title_temp.html", 'r') as f:
            head = f.read()
        with open("encyclopedia/templates/encyclopedia/title.html", "w") as f:
            f.write(head)
        with open("encyclopedia/templates/encyclopedia/title.html", "a") as f:
            f.write(content)
            f.write("\n{% endblock %}")
        return render(request, "encyclopedia/title.html", {
            "title": title,
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "message": f'Page for "{title}" not found!'
        })

def new(request):
    if request.method == "POST":
        form = NewTitle(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            if util.get_entry(new_title):
                return render(request, "encyclopedia/error.html", {
                    "message": "Title exists already.",
                    "title": new_title
                })
            content = form.cleaned_data["content"]
            with open(f"entries/{new_title}.md", "a") as f:
                header = '# ' + new_title + '\n \n'
                f.write(header)
                f.write(content)
            return redirect("title", title=new_title)
    return render(request, "encyclopedia/new.html", {
        "form": NewTitle()
    })

def edit(request, title):
    if request.method == "POST":       
        #update title content
        form = updateTitle(request.POST)
        if form.is_valid():
            content = form.cleaned_data['newContent']
            content = content.replace('\n', '', 3)
            with open(f"entries/{title}.md", "w") as f:
                f.write(content)
            return redirect("title", title = title)
        else:
            return HttpResponse("error!")
    preContent = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": updateTitle(initial={"newContent": preContent})
    })


def search(request):
    if request.method == "POST":
        #sidebar search
        search_title = request.POST.get("q", None)
        if search_title:
            entry = util.get_entry(search_title)
            if entry:
                return redirect("title", title=search_title)
            else:
                title_list = util.list_entries()
                title_match = []
                for element in title_list:
                    if re.match(f".*{search_title.upper()}.*", element.upper()):
                        title_match.append(element)
                if title_match:
                    return render(request, "encyclopedia/search.html", {
                        "title": search_title,
                        "matches": sorted(title_match),
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "message": "No match title found!"})

def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect('title', title = title)





    
