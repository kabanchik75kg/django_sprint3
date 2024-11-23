import datetime

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели дату создания и параметр,
    указывающий на статус публикации содержимого.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField('Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(User, models.CASCADE,
                               verbose_name='Автор публикации')
    location = models.ForeignKey(Location, models.SET_NULL, null=True,
                                 blank=True, verbose_name='Местоположение')
    category = models.ForeignKey(Category, models.SET_NULL, null=True,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    @classmethod
    def active_post(cls):
        """Возвращает QuerySet всех постов модели Post,
        которые удовлетворяют требованиям.

        Метод фильтрует объекты модели Post, возвращая только те,
        у которых:
            дата публикации — не позже текущего времени,
            он опубликован,
            категория, к которой он принадлежит, не снята с публикации;
        А также объединяет таблицы: location, author, category

        Returns:
            QuerySet: Объекты, строками которых является
            объединение всех таблиц и выборка по критериям.
        """
        return cls.objects.filter(
            pub_date__lte=datetime.datetime.now(),
            is_published=True,
            category__is_published=True
        ).select_related('location', 'author', 'category')
