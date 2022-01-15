# Generated by Django 3.2.8 on 2021-11-11 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_alter_place_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geomodel',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Ad'),
        ),
        migrations.AlterField(
            model_name='geomodel',
            name='place',
            field=models.IntegerField(blank=True, choices=[(1, 'Hastane'), (2, 'Market'), (3, 'Restorant'), (4, 'Okul'), (5, 'Benzinlik'), (6, 'Diğer')], null=True),
        ),
    ]
