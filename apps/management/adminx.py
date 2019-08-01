import xadmin

from .models import Menu


class MenuAdmin(object):
    list_display = ['name', 'submenu', 'url', 'parentmenu', 'icon', 'seq']
    search_fields = ['name', 'submenu', 'url', 'parentmenu', 'icon', 'seq']
    list_filter = ['name', 'submenu', 'url', 'parentmenu', 'icon', 'seq']


xadmin.site.register(Menu, MenuAdmin)