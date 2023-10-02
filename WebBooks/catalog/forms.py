from django import forms
from datetime import date
from .models import Book

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label=('First Name'), max_length=50)
    last_name = forms.CharField(label=('Last Name'), max_length=100)
    date_of_birth = forms.DateField(label=('Date of Birth'), initial = format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'})
                                    )
    date_of_death = forms.DateField(label=('Date of Death'), initial = format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'})
                                    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']

