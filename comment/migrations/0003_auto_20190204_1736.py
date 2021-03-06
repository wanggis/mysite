# Generated by Django 2.1.5 on 2019-02-04 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20190202_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-comment_time']},
        ),
        migrations.AddField(
            model_name='comment',
            name='parrent_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='comment.Comment'),
        ),
    ]
