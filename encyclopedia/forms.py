from django import forms

# Class for creating entries.
# Includes two fields.  One for the title, one for the content.
class EntryForm(forms.Form):
    my_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "This displays in the tab"}),
    )
    my_markdown_data = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Enter markdown content here.  This is the viewed entry"}
        )
    )

    def clean_data(self):
        data_title = self.cleaned_data["my_title"]
        data_markdown = self.cleaned_data["my_markdown_textarea"]
        return (data_title, data_markdown)

# Class for editing entries.
# Includes one field for editing the content.
class EditForm(forms.Form):
    my_markdown_textarea = forms.CharField(widget=forms.Textarea())

    def clean_data(self):
        data_markdown = self.cleaned_data["my_markdown_textarea"]
        return data_markdown
