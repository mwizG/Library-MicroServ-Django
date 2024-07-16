from . models import Books,Authors
from django import forms


class BookForm(forms.ModelForm):
    # Define form fields with specific types and attributes
    pub_year = forms.DateField(label="Date published", input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}))
    coverimg = forms.CharField(max_length=200, required=False)
    rating = forms.IntegerField(required=False)
    genre = forms.CharField(max_length=200, required=False)
    author = forms.ModelChoiceField(queryset=Authors.objects.all(), required=False, empty_label="---------")

    class Meta:
        model = Books
        fields = '__all__'

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = '__all__'