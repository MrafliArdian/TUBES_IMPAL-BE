<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# artikel/views.py
from rest_framework import viewsets, permissions
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # izin akses:
    # - list, retrieve  -> boleh umum (Home / halaman Artikel di UI)
    # - create, update, delete -> harus login (JWT)
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # set author otomatis dari user yang login
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
>>>>>>> 44da526b83f40d4dc6b1ef904768a5b18d335807
