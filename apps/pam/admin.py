from django.contrib import admin
from django import forms

from .forms import PamUserForm
from .models import FtpPamUser, SftpPamUser, PamGroups, PamGroupLists
# Register your models here.
admin.site.site_title = 'FSHAMS'
admin.site.site_header = 'FSHAMS'
admin.site.index_title  = 'FSHAMS'

class FtpPamUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'uid', 'gid', 'shell')
    form = PamUserForm
    def get_queryset(self, request):
        qs = super(FtpPamUserAdmin, self).get_queryset(request)
        qs = qs.filter(gid=6000)
        return qs


class SftpPamUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'uid', 'gid', 'shell')
    form = PamUserForm
    def get_queryset(self, request):
        qs = super(SftpPamUserAdmin, self).get_queryset(request)
        qs = qs.filter(gid=5000)
        return qs

class PamGroupsAdmin(admin.ModelAdmin):
    list_display = ('name',  'gid')

class GroupListsAdmin(admin.ModelAdmin):
    list_display = ('username', 'gid')

admin.site.register(FtpPamUser, FtpPamUserAdmin)
admin.site.register(SftpPamUser, SftpPamUserAdmin)
admin.site.register(PamGroups, PamGroupsAdmin)
admin.site.register(PamGroupLists, GroupListsAdmin)