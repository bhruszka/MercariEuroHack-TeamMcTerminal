# Generated by Django 2.1.2 on 2018-10-20 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20181020_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='img', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='facebook_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
