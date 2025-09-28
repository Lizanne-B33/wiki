from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
from . import util
from . import forms


def index(request):
    return render(
        request, "encyclopedia/index.html", {"entries": util.list_entries()}
    )


def single_entry_view(request, filename):
    ###
    # This function handles the display of a single entry.
    # If the entry exists, it renders the entry page.
    # If not, it renders the entry not found page.
    ###
    my_title = filename.rsplit(".", 1)[0]
    try:
        markdown_content = util.get_entry(my_title)
        if markdown_content is None:
            raise FileNotFoundError
        html_content = markdown.markdown(markdown_content)
        context = {"single_entry": html_content, "my_title": my_title}
        return render(
            request, "encyclopedia/single_entry.html", context=context
        )
    except:
        return render(
            request, "encyclopedia/not_found.html", {"my_title": my_title}
        )


def search_view(request):
    ###
    # This function handles the search capability of the application .
    # If the search value exists, it renders the entry page.
    # If the user enters a partial (ex. oth) then entries with that value
    # as part of the title will be listed with a hyperlink to display the entry.
    # If the user enters a value not in the list, it renders the "oops" page.
    ###
    my_criteria = request.GET.get("q")
    exists = util.get_entry(my_criteria)
    if exists == None:
        partial = util.search_entry(my_criteria)
        if not partial:
            return render(
                request,
                "encyclopedia/not_exist.html",
                {"criteria": my_criteria},
            )
        else:
            return render(
                request, "encyclopedia/index.html", {"entries": partial}
            )
    else:
        markdown_content = util.get_entry(my_criteria)
        html_content = markdown.markdown(markdown_content)
        context = {"single_entry": html_content, "my_title": my_criteria}
        return render(
            request, "encyclopedia/single_entry.html", context=context
        )


def add_view(request):

    if request.method == "POST":
        my_form = forms.EntryForm(request.POST)
        if my_form.is_valid():
            my_title = my_form.cleaned_data["my_title"]
            my_title = my_title.replace(" ", "_")
            my_markdown_data = my_form.cleaned_data["my_markdown_data"]
            add = util.new_entry(my_title, my_markdown_data)

            if add == "Created":
                return render(
                    request, "encyclopedia/added.html", {"title": my_title}
                )
            else:
                return render(
                    request, "encyclopedia/exists.html", {"title": my_title}
                )
        else:
            return render(request, "encyclopedia/error.html")

    else:
        my_form = forms.EntryForm()
        return render(request, "encyclopedia/add.html", {"form": my_form})


def edit_view(request, filename):
    my_title = filename

    if request.method == "POST":
        my_form = forms.EditForm(request.POST)
        if my_form.is_valid():
            my_markdown_data = my_form.cleaned_data["my_markdown_textarea"]
            add = util.save_entry(my_title, my_markdown_data)
            return redirect("single_entry", filename=my_title)
    else:
        initial_data = {"my_markdown_textarea": util.get_entry(my_title)}
        print(initial_data)
        my_form = forms.EditForm(initial=initial_data)
        return render(
            request,
            "encyclopedia/edit.html",
            {
                "my_title": my_title,
                "initial": initial_data,
                "form": my_form,
            },
        )


def random_view(request):
    my_title = util.random_entry()
    markdown_content = util.get_entry(my_title)
    html_content = markdown.markdown(markdown_content)
    context = {"single_entry": html_content, "my_title": my_title}
    return render(request, "encyclopedia/single_entry.html", context=context)
