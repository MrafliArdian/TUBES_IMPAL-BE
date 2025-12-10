# artikel/models.py
from django.db import models
from django.conf import settings


class Article(models.Model):
    article_id = models.BigAutoField(
        primary_key=True,
        db_column='article_id'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='author_id',
        related_name='articles'
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles'      # tabel MySQL yang sudah ada
        ordering = ['-created_at']

    def __str__(self):
        return self.title

