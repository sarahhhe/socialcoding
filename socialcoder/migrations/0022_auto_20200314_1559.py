# Generated by Django 2.2.7 on 2020-03-14 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialcoder', '0021_auto_20200314_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
