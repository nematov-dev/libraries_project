# Generated by Django 5.1.7 on 2025-03-31 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library',
            old_name='librarian',
            new_name='user',
        ),
    ]
