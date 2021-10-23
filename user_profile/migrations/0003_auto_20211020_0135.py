# Generated by Django 3.2.6 on 2021-10-19 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0004_rename_uuid_id_material_uuid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0002_alter_profile_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='materials_claimed',
            field=models.ManyToManyField(related_name='profiles', to='Post.Material'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]
