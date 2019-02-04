# Generated by Django 2.0.10 on 2019-02-04 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190204_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='blog_tag',
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_tag',
            field=models.ManyToManyField(to='blog.BlogTag', verbose_name='标签'),
        ),
    ]
