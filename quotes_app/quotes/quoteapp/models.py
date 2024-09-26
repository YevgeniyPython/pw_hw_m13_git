from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.DateField(blank=True, null=True)
    born_location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    tags = models.ManyToManyField(Tag, related_name='quotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'"{self.text[:50]}" - {self.author.fullname}'

