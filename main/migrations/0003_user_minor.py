# Generated by Django 5.1.2 on 2024-10-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_profile_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='minor',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
