from django.db import models
from django.db.models import Func, Value
from django import forms
from sympy import false


class DbEncrypt(Func):
    function = 'ENCRYPT'


# Create pam_mysql models.
# includes users、groups、grouplist、log
# https://github.com/NigelCunningham/pam-MySQL/blob/master/examples/users.sql
class PamUsers(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False, default=None)
    password = models.CharField(max_length=160, null=False, blank=False)
    shell = models.CharField(max_length=20, null=False, blank=False, default='/usr/bin/false')
    status = models.CharField(max_length=1, null=False, blank=True, default='N')
    uid = models.IntegerField(null=False, blank=False, primary_key=True)
    gid = models.IntegerField(null=False, blank=False, default=5000)
    gecos = models.CharField(max_length=128, null=True, blank=True)
    homedir = models.CharField(max_length=32, null=True, blank=True)
    lstchg = models.IntegerField(null=False, blank=True, default=-1)
    min = models.IntegerField(null=False, blank=True, default=0)
    max = models.IntegerField(null=False, blank=True, default=9999)
    warn = models.IntegerField(null=False, blank=True, default=7)
    inact = models.IntegerField(null=False, blank=True, default=-1)
    expire = models.IntegerField(null=False, blank=True, default=-1)
    flag = models.IntegerField(null=False, blank=True, default=-1)

    #def save(self, *args, **kwargs):
    #    self.password = DbEncrypt(Value('password'))

    def set_password(self, password):
        self.password = DbEncrypt(Value('password'))

    def check_password(self, password):
        self.password = DbEncrypt(password)

    class Meta:
        db_table = 'users'


class SftpPamUser(PamUsers):
    class Meta:
        proxy = True
        verbose_name = 'SFTP User'
        verbose_name_plural = verbose_name


class FtpPamUser(PamUsers):
    class Meta:
        proxy = True
        verbose_name = 'FTP User'
        verbose_name_plural = verbose_name


class PamGroups(models.Model):
    name = models.CharField(max_length=30, null=True, blank=False)
    gid = models.IntegerField(null=False, blank=False, primary_key=True)
    status = models.CharField(max_length=1, null=False, blank=True, default='A')
    password = models.CharField(max_length=64, null=True, blank=True, default='x')

    '''
    Default set gid 5000 and autoincrement.
    '''

    def save(self, *args, **kwargs):
        if not self.pk:
            last_gid = PamGroups.objects.order_by('gid').first()
            self.gid = last_gid.gid + 1 if last_gid else 5000

    class Meta:
        db_table = 'groups'
        verbose_name = 'Pam Groups'
        verbose_name_plural = verbose_name


class GroupLists(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    gid = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        db_table = 'grouplists'


class PamLog(models.Model):
    logid = models.AutoField(primary_key=True)
    time = models.DateTimeField(null=False, blank=True, auto_now=True)
    user = models.CharField(max_length=50, null=False, blank=False)
    pid = models.IntegerField(null=False, blank=False)
    host = models.CharField(max_length=100, null=False, blank=False)
    rhost = models.TextField(max_length=100, null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'log'
