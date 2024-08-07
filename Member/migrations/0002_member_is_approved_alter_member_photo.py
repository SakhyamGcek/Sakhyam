# Generated by Django 5.0.7 on 2024-08-03 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='members/'),
        ),
    ]
