from django.shortcuts import render

from . import util

import re

from markdown2 import Markdown


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
            "message": "Title not found!"
        })