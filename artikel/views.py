
from django.shortcuts import render

# Create your views here.
# artikel/views.py
from rest_framework import viewsets, permissions
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk artikel.
    
    Permissions:
    - List & Retrieve: AllowAny (semua orang bisa lihat artikel)
    - Create, Update, Delete: IsAdminUser (hanya admin dengan is_staff=True)
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """
        Atur permissions berdasarkan action:
        - list, retrieve: boleh umum (tanpa login)
        - create, update, partial_update, destroy: hanya admin
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # Hanya admin (is_staff=True) yang bisa create/update/delete
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        # Set author otomatis dari user yang login (admin)
        serializer.save(author=self.request.user)
