from django.shortcuts import render, redirect
from django.urls import reverse
from . import util

import re

from markdown2 import Markdown


def index(request):
    if request.method == "POST":
        title = request.POST["q"]
        entry = util.get_entry(title)
        if entry:
            return redirect("title", title=title)
        else:
            title_list = util.list_entries()
            title_match = []
            for element in title_list:
                if re.match(f".*{title.upper()}.*", element.upper()):
                    title_match.append(element)
            if title_match:
                return render(request, "encyclopedia/search.html", {
                    "title": title,
                    "matches": sorted(title_match),
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No match title found!"})        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if request.method == "POST":
        search_title = request.POST["q"]
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