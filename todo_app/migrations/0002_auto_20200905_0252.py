# Generated by Django 3.1.1 on 2020-09-05 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date_finished',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]