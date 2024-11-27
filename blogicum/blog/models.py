from constants import Constant
from django.contrib.auth import get_user_model
from django.db import models

from .managers import PublishedPost
from .utils import trancate_words

User = get_user_model()


class BaseModel(models.Model):
    """
    Абстрактная модель, предоставляющая базовые поля для других моделей.

    Добавляет к модели дату создания и параметр,
    указывающий на статус публикации содержимого.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )

    class Meta:
        abstract = True
        ordering = ["created_at"]


class Location(BaseModel):
    name = models.CharField(
        max_length=Constant.MAX_STRING_LENGTH,
        verbose_name="Название места"
    )

    class Meta(BaseModel.Meta):
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return trancate_words(self.name, Constant.MAX_DISPLAY_LETTERS)


class Category(BaseModel):
    title = models.CharField(
        max_length=Constant.MAX_STRING_LENGTH,
        verbose_name="Заголовок"
    )
    description = models.TextField("Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta(BaseModel.Meta):
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return trancate_words(self.title, Constant.MAX_DISPLAY_LETTERS)


class Post(BaseModel):
    title = models.CharField(
        max_length=Constant.MAX_STRING_LENGTH,
        verbose_name="Заголовок"
    )
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        verbose_name="Автор публикации")
    location = models.ForeignKey(
        Location,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение"
    )
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name='posts'
    )

    objects = models.Manager()
    published_posts = PublishedPost()

    class Meta(BaseModel.Meta):
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-pub_date']

    def __str__(self):
        return trancate_words(self.title, Constant.MAX_DISPLAY_LETTERS)
