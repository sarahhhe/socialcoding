# Generated by Django 2.2.7 on 2020-03-12 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialcoder', '0008_auto_20200312_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='clique',
            new_name='category',
        ),
    ]
