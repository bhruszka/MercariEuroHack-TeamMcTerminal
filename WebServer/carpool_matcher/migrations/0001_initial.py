# Generated by Django 2.1.2 on 2018-10-20 23:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance', models.IntegerField()),
                ('time', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('capacity', models.IntegerField(default=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drivers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('longitude', models.CharField(max_length=15)),
                ('latitude', models.CharField(max_length=15)),
                ('all_distances_calculated', models.BooleanField(default=False)),
                ('order_in_route', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='carpool_matcher.Driver')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance', models.IntegerField(null=True)),
                ('time', models.IntegerField(null=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='carpool_matcher.Driver')),
                ('end_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_end_routes', to='carpool_matcher.Location')),
                ('passenger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='carpool_matcher.Passenger')),
                ('start_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_start_routes', to='carpool_matcher.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='distance',
            name='end_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_end_distances', to='carpool_matcher.Location'),
        ),
        migrations.AddField(
            model_name='distance',
            name='start_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_start_distances', to='carpool_matcher.Location'),
        ),
    ]
