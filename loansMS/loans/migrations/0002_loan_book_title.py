# Generated by Django 5.0.2 on 2024-07-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='book_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
