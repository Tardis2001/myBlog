# Generated by Django 5.1.2 on 2024-10-24 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblogapp', '0005_post_thumbnail_alter_comment_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='/placeholder.svg', upload_to='media/'),
        ),
    ]
