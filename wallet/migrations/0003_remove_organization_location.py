# Generated by Django 4.1.3 on 2022-11-16 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_remove_transaction_category_delete_categories_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='location',
        ),
    ]