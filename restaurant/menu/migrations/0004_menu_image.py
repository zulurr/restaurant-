# Generated by Django 5.0.6 on 2024-11-26 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_remove_sumorder_created_at_sumorder_created_at_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
