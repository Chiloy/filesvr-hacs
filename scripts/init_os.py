import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hams.settings')
# 很关键的配置
django.setup()