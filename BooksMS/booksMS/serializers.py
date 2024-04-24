from rest_framework import serializers
from .models import Books

class BooksSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Books
        fields = ['id', 'title', 'pub_year', 'coverimg', 'rating', 'genre', 'author', 'author_name']
