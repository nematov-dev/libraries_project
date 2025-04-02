from django.db import models

from app_auth.models import Library

class Book(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    publisher = models.CharField(max_length=255)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="books")
    quantity_in_library = models.PositiveIntegerField(default=1)

    def __str__(self):
        self.name

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

