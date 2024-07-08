from . models import Loan
from django import forms


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['return_date', 'user_id', 'book_id']
        widgets = {
            'user_id': forms.HiddenInput(),
            'book_id': forms.HiddenInput(),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

