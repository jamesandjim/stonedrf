import xadmin

from .models import Device


class DeviceAdmin(object):
    list_display = ['name', 'sn', 'ip', 'netmask', 'netgate', 'mac', 'ver']
    search_fields = ['name', 'sn', 'ip', 'netmask', 'netgate', 'mac', 'ver']
    list_filter = ['name', 'sn', 'ip', 'netmask', 'netgate', 'mac', 'ver']


xadmin.site.register(Device, DeviceAdmin)
