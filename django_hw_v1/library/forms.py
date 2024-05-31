from django import forms
from django.core import validators

alphanumeric_validator = validators.RegexValidator(
    regex=r"^[a-zA-Z0-9 ]*$", message="Only letters, numbers, and spaces are allowed."
)
alphabetic_space_validator = validators.RegexValidator(
    regex=r"^[a-zA-Z ]*$", message="Only alphabetic characters and spaces are allowed."
)


class BookSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100, required=False, initial="", validators=[alphanumeric_validator]
    )
    author = forms.CharField(
        max_length=100,
        required=False,
        initial="",
        validators=[alphabetic_space_validator],
    )
    category = forms.CharField(max_length=100, required=False, initial="")
    available_only = forms.BooleanField(required=False, initial=False)
