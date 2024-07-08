from . models import Books,Authors
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = '__all__'