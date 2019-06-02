from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nickname', 'avatar', 'position', 'work_year', 'personal_url', 'role', 'created_at', 'updated_at']
    search_fields = ['username', 'nickname', 'position']
    list_filter = ['work_year', 'role', 'created_at', 'updated_at']
    list_per_page = 50
    ordering = ['-created_at']


admin.site.site_header = "Ahern's Blog 后台管理"
admin.site.site_title = "Ahern's Blog"
