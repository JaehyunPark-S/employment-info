# Generated by Django 3.1.7 on 2021-04-12 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20210412_2239'),
        ('users', '0012_auto_20210412_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_boards',
            field=models.ManyToManyField(blank=True, related_name='users', to='boards.Board'),
        ),
    ]
