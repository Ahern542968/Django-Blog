import xadmin
from xadmin import views

from .models import Author


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = 'Ahern Blog'
    site_footer = 'Ahern Blog'
    menu_style = 'accordion'


class AuthorAdmin(object):
    list_display = ['author']
    list_filter = ['author']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Author, AuthorAdmin)
