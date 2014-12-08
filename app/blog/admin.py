from django.contrib import admin
from blog.models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created", "last_updated")


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
