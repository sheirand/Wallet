# Generated by Django 4.1.3 on 2022-11-09 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_categories_user_categories'),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='user.categories'),
        ),
    ]