# Generated by Django 2.2.7 on 2020-04-09 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialcoder', '0031_auto_20200408_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='content',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
