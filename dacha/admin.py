from django.contrib import admin
from . import models

# admin.site.register(models.Material)
admin.site.register(models.Comment)
admin.site.register(models.Profile)


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'material_type', 'publish')
    list_filter = ('material_type', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('material_type', 'title')


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
