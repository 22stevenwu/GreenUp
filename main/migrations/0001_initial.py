# Generated by Django 4.2.16 on 2024-10-21 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('major', models.CharField(max_length=255)),
                ('gradyear', models.PositiveIntegerField()),
            ],
        ),
    ]
