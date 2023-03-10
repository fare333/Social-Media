# Generated by Django 4.1.3 on 2023-02-21 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0018_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(blank=True, to='social.tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='social.tag'),
        ),
    ]
