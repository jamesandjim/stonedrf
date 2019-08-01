from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=50, verbose_name='菜单名称')
    submenu = models.CharField(max_length=1, default='0', verbose_name='是否有子菜单')
    parentmenu = models.CharField(max_length=50, verbose_name='父菜单')
    url = models.CharField(max_length=50, verbose_name='菜单链接地址')
    icon = models.CharField(max_length=16, verbose_name='菜单图标', null=True, blank=True)
    seq = models.CharField(max_length=4, verbose_name='排序')

    class Meta:
        verbose_name = '系统菜单'
        verbose_name_plural = verbose_name