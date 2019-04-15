# Generated by Django 2.2 on 2019-04-15 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BtCollector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('source', models.URLField()),
                ('link', models.TextField()),
                ('size', models.CharField(max_length=15)),
                ('seeder', models.PositiveIntegerField()),
                ('leecher', models.PositiveIntegerField()),
                ('site', models.CharField(max_length=15)),
                ('search', models.CharField(max_length=63)),
                ('cat', models.CharField(default='all', max_length=15)),
            ],
        ),
    ]