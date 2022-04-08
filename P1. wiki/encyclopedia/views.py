from dataclasses import fields
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm, Textarea
import random

from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    if entry == None :
        entryHTML = "<p>The page you requested doesn't exist.</p>"
    else :
        markdowner = Markdown()
        entryHTML = markdowner.convert(entry)
        
    return render(request, "encyclopedia/entry.html", {
        "entry": entryHTML,
        "title": title
    })

def search(request):
    query = request.POST['q']
    entries = util.list_entries()
    suggestions = []
    for entry in entries:
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry", kwargs={'title': query}))
        if query.lower() in entry.lower():
            suggestions.append(entry)
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "suggestions": suggestions
    })

class NewEntry(forms.Form):
        title = forms.CharField(label="title")
        content = forms.CharField(widget=forms.Textarea)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['content'].widget.attrs.update({'style': 'height: 100%;'})
            self.fields['content'].widget.attrs.update({'rows': 20})

def new_entry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/error.html", {
                        'message': 'The entry already exist. Try editing the existing entry.'
                    } )
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    
    return render(request, "encyclopedia/new_entry.html", {
        "form" : NewEntry()
    })

def edit_entry(request, title):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "form" : NewEntry({'title':title, 'content':content})
    })

def random_entry(request):
    randomEntry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={'title': randomEntry}))