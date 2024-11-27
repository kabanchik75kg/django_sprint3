from django.contrib import admin

from .models import Category, Location, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ("title", "slug", "is_published")
    list_editable = ("is_published",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ("name", "is_published")
    list_editable = ("is_published",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "pub_date",
        "author",
        "location",
        "category",
        "is_published",
        "created_at",
    )
    list_editable = ("pub_date", "is_published", "author")
    search_fields = ("title", "author")
    list_filter = ("title", "author", "category")
    empty_value_display = "Не указано"
