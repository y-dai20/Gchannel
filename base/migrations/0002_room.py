# Generated by Django 3.2.5 on 2022-07-17 12:09

import base.models.functions
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.CharField(default=base.models.functions.create_id, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255)),
                ('subtitle', models.CharField(default='', max_length=255)),
                ('img', models.ImageField(blank=True, null=True, upload_to=base.models.functions.img_directory_path)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]