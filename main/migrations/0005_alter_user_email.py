# Generated by Django 5.1.2 on 2024-10-21 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='rikka0612@gmail.com', max_length=254),
        ),
    ]
