# Generated by Django 2.1.5 on 2019-02-04 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20190204_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parrent',
            new_name='parent',
        ),
    ]
