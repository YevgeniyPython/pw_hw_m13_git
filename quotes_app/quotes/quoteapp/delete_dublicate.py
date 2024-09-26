import models
from .models import Author
# Получаем всех авторов с одинаковыми именами
duplicate_authors = Author.objects.values('fullname').annotate(name_count=models.Count('fullname')).filter(name_count__gt=1)

for author in duplicate_authors:
    # Удаляем все дубликаты кроме одного
    Author.objects.filter(fullname=author['fullname']).exclude(pk=Author.objects.filter(fullname=author['fullname']).first().pk).delete()
