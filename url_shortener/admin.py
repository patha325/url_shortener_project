from django.contrib import admin
from .models import URL

class URLAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_url', 'short_url', 'clicks', 'created_at')
    search_fields = ('original_url', 'short_url', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(URL, URLAdmin)