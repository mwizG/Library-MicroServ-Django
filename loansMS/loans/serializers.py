from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [ 'book_id','book_title', 'loan_date', 'return_date', 'returned']
