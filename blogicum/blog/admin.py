from django.contrib import admin

from .models import Category, Post, Location


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ('title', 'slug', 'is_published')
    list_editable = ('is_published', )


class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline, )
    list_display = ('name', 'is_published')
    list_editable = ('is_published', )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'pub_date',
        'is_published',
        'author'
    )
    search_fields = (
        'title',
        'author'
    )
    list_filter = (
        'title',
        'author',
        'category'
    )
    empty_value_display = 'Не указано'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
