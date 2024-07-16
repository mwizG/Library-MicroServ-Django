from rest_framework import serializers
from .models import Books  # Assuming Books is the model name

class BooksSerializer(serializers.ModelSerializer):
    # Define author_name field using CharField to fetch author's name from related model (read-only)
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Books  # Specify the model to serialize
        # Specify fields to include in the serialized output
        fields = ['id', 'title', 'pub_year', 'coverimg', 'rating', 'genre', 'author', 'author_name']
