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
            'description',      # Description/summary artikel
            'content',
            'image_url',
            'source_link',      # Link ke sumber berita
            'created_at',
            'updated_at',
            'author',           # id user
            'author_name',      # username, hanya untuk dibaca
        ]
        read_only_fields = ['article_id', 'created_at', 'updated_at', 'author', 'author_name']
