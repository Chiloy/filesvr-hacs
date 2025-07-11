from django.db import models
from django.db.models import Func, Value
from django.dispatch import receiver
from dotenv import load_dotenv
import os

from zeroconf import instance_name_from_service_info

# Load environment variables from .env file
load_dotenv()
FAHACS_FILE_ROOT_DIR = os.getenv('FAHACS_FILE_ROOT_DIR')

class DbEncrypt(Func):
    function = 'ENCRYPT'


# Create pam_mysql models.
# includes users、groups、grouplist、log
# https://github.com/NigelCunningham/pam-MySQL/blob/master/examples/users.sql

class PamGroups(models.Model):
    name = models.CharField(max_length=30, blank=False)
    gid = models.IntegerField(null=False, blank=False, primary_key=True, unique=True)
    status = models.CharField(max_length=1, null=False, blank=True, default='A')
    password = models.CharField(max_length=64, null=True, blank=True, default='x')

    def __str__(self):
        return self.name
    '''
    Default set gid 5000 and autoincrement.
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_gid = PamGroups.objects.order_by('gid').first()
            self.gid = last_gid.gid + 1 if last_gid else 5000
    '''

    class Meta:
        db_table = 'groups'
        verbose_name = 'Pam Groups'
        verbose_name_plural = verbose_name

class PamUsers(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False, primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=False, blank=True)
    password = models.CharField(max_length=160, null=False, blank=False)
    shell = models.CharField(max_length=20, null=False, blank=False, default='/usr/bin/false')
    status = models.CharField(max_length=1, null=False, blank=True, default='N')
    uid = models.IntegerField(null=False, blank=False)
    # gid = models.IntegerField(null=False, blank=False, default=5000)
    gid = models.ForeignKey(PamGroups, on_delete=models.CASCADE, null=False, blank=False,
                            db_column='gid', verbose_name='Group')
    gecos = models.CharField(max_length=128, null=True, blank=True)
    homedir = models.CharField(max_length=32, null=True, blank=True)
    lstchg = models.IntegerField(null=False, blank=True, default=-1)
    min = models.IntegerField(null=False, blank=True, default=0)
    max = models.IntegerField(null=False, blank=True, default=9999)
    warn = models.IntegerField(null=False, blank=True, default=7)
    inact = models.IntegerField(null=False, blank=True, default=-1)
    expire = models.IntegerField(null=False, blank=True, default=-1)
    flag = models.IntegerField(null=False, blank=True, default=-1)

    def save(self, *args, **kwargs):
        self.homedir = os.path.join(FAHACS_FILE_ROOT_DIR, str(self.gid), self.username)
        self.password = DbEncrypt(Value('password'))
        super(PamUsers, self).save(*args, **kwargs)

    def set_password(self, password):
        self.password = DbEncrypt(Value('password'))

    def check_password(self, password):
        self.password = DbEncrypt(password)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class PamGroupLists(models.Model):
    username = models.OneToOneField(PamUsers, on_delete=models.CASCADE, db_column='username',
                                 primary_key=True)
    gid = models.ForeignKey(PamGroups, on_delete=models.CASCADE, db_column='gid')

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = 'grouplists'
        verbose_name = 'Group Lists'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'gid'], name='unique_grouplists_username_gid'
            )
        ]


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

@receiver (models.signals.post_save, sender=PamUsers)
def create_pam_user(sender, instance, created, **kwargs):
    if created:
        print(instance)
        #pam_grp_list_inst = PamGroupLists.objects.create(username=username, gid=self.gid)
        #pam_grp_list_inst.save()

@receiver (models.signals.post_save, sender=SftpPamUser)
def create_pam_user(sender, instance, created, **kwargs):
    if created:
        # if table column had foreignKey need instance.
        grp_instance = PamGroups.objects.filter(name=instance.gid).first()
        user_instance = PamUsers.objects.filter(username=instance.username).first()
        PamGroupLists.objects.create(username=user_instance, gid=grp_instance).save()