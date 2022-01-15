# Generated by Django 3.2.8 on 2021-10-22 07:18

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=250)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('line', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
    ]