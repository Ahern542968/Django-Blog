import xadmin
from xadmin import views

from .models import UserActiveCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = 'Ahern\'s Blog'
    site_footer = 'Ahern\'s Blog'
    menu_style = 'accordion'


class UserProfileAdmin(object):
    list_display = ['id', 'nickname', 'username', 'email', 'is_active', 'is_super', 'date']
    search_fields = ['id', 'nickname', 'username', 'email', 'is_active', 'is_super']
    list_filter = ['is_active', 'is_super']


class UserActiveCodeAdmin(object):
    list_display = ['id', 'email', 'send_for', 'code', 'date']
    search_fields = ['email', 'send_for', 'code']
    list_filter = ['email', 'send_for', 'date']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(UserActiveCode, UserActiveCodeAdmin)
