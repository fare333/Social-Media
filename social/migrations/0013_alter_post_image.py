# Generated by Django 4.1.3 on 2023-02-21 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_image_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, to='social.image'),
        ),
    ]
