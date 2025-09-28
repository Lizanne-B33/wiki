# This file holds the form classes that are used in the application.

from django import forms

# Class for creating entries.
# This form includes two fields.  One for the title and one for the content.
# It also includes the functions to clean the data prior to saving.


class EntryForm(forms.Form):
    my_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "This displays in the tab"}
        ),
    )
    my_markdown_data = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Enter markdown content here."}
        )
    )

    def clean_data(self):
        data_title = self.cleaned_data["my_title"]
        data_markdown = self.cleaned_data["my_markdown_textarea"]
        return (data_title, data_markdown)


# Class for editing entries.
# This form includes one field for editing the content.
# It also includes the functions to clean the data prior to saving.


class EditForm(forms.Form):
    my_markdown_textarea = forms.CharField(widget=forms.Textarea())

    def clean_data(self):
        data_markdown = self.cleaned_data["my_markdown_textarea"]
        return data_markdown
