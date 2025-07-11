import os
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from .models import SftpPamUser, FtpPamUser, PamGroups, PamUsers, PamGroupLists
from django.contrib.auth.models import User
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
FAHACS_PAM_GROUPS_NAME = os.getenv('FAHACS_PAM_GROUPS_NAME')

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='Fshacs@cn',
            email='admin@fahacs.com'
        )

@receiver(post_migrate)
def create_pam_groups(sender, **kwargs):
    for group_name in FAHACS_PAM_GROUPS_NAME.split(','):
        if not PamGroups.objects.filter(name=group_name).exists():
            PamGroups.objects.create()

@receiver(post_save, sender=FtpPamUser)
def create_pam_user(sender, instance, created, **kwargs):
    if created:
        # if table column had foreignKey need instance.
        grp_instance = PamGroups.objects.filter(name=instance.gid).first()
        user_instance = PamUsers.objects.filter(username=instance.username).first()
        PamGroupLists.objects.create(username=user_instance, gid=grp_instance).save()


@receiver(post_save, sender=SftpPamUser)
def create_pam_user(sender, instance, created, **kwargs):
    if created:
        # if table column had foreignKey need instance.
        grp_instance = PamGroups.objects.filter(name=instance.gid).first()
        user_instance = PamUsers.objects.filter(username=instance.username).first()
        PamGroupLists.objects.create(username=user_instance, gid=grp_instance).save()