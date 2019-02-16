import xadmin
from xadmin import views

from .models import UserProfile


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


# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
