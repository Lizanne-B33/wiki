from django.shortcuts import render
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
        return render(request, "encyclopedia/not_found.html", {"my_title": my_title})


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
        my_form = forms.entry_form(request.POST)
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
        my_form = forms.entry_form()
        return render(request, "encyclopedia/add.html", {"form": my_form})

def edit_view(request, filename):
    ###
    # This function renders the entry_form so that the user can add a new entry.
    # If this is a POST request then process the Form data, else it renders
    # the form for the user to input data with the existing content ready for edit.
    ###
    my_title = filename.rsplit(".", 1)[0]
    initial_data = {"markdown_data": util.get_entry(my_title)}

    if request.method == "POST":

        # Create a form instance and populate it with data from the request
        my_form = entry_form(request.POST)

        # Check if the form is valid:
        if my_form.is_valid():

            # process the data in form.cleaned_data as required
            my_markdown_data = my_form.cleaned_data["markdown_data"]

            # Calls the save_entry function to save the file.
            add = util.save_entry(my_title, my_markdown_data)
    else:
        edit = util.edit_entry(my_title)
        if edit != None:
            my_form = forms.edit_form(request.POST, initial=initial_data)
            return render(request, "encyclopedia/edit.html", {"form": my_form})
        else:
            return render(request, "error")

def random_view(request):
    my_title = util.random_entry()
    markdown_content = util.get_entry(my_title)
    html_content = markdown.markdown(markdown_content)
    context = {"single_entry": html_content, "my_title": my_title}
    return render(
            request, "encyclopedia/single_entry.html", context=context
    )

