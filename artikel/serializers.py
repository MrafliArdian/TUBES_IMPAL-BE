# artikel/serializers.py
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Article
        fields = [
            'article_id',
            'title',
            'content',
            'image_url',
            'created_at',
            'author',       # id user
            'author_name',  # username, hanya untuk dibaca
        ]
        read_only_fields = ['article_id', 'created_at', 'author', 'author_name']
