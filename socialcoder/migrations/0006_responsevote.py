# Generated by Django 2.2.7 on 2020-02-20 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialcoder', '0005_response_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialcoder.Response')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
