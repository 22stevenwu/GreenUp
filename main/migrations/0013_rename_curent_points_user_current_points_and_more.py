# Generated by Django 5.1.2 on 2024-11-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_campaigncompletion_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='curent_points',
            new_name='current_points',
        ),
        migrations.AddField(
            model_name='user',
            name='completed_campaigns',
            field=models.ManyToManyField(blank=True, related_name='users', to='main.campaign'),
        ),
        migrations.DeleteModel(
            name='CampaignCompletion',
        ),
    ]