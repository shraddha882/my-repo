# Generated by Django 4.0.2 on 2024-01-02 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_profile_is_approved_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
