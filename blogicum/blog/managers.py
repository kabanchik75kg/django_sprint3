from django.db import models
from django.utils import timezone


class PublishedPost(models.Manager):
    """
    Менеджер для выборки опубликованных постов.

    Менеджер фильтрует посты, у которых:
        дата публикации — не позже текущего времени,
        он опубликован,
        категория, к которой он принадлежит, не снята с публикации;
    А также объединяет таблицы: location, author, category
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            )
            .select_related("location", "author", "category")
        )
