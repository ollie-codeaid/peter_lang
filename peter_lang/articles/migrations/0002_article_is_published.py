# Generated by Django 2.0.9 on 2019-03-31 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
