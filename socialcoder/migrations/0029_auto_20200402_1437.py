# Generated by Django 2.2.7 on 2020-04-02 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialcoder', '0028_auto_20200402_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='upvotes',
        ),
    ]
