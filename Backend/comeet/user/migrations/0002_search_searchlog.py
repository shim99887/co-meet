# Generated by Django 3.0.5 on 2021-03-31 01:27

from django.db import migrations, models
import djongo.models.fields
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('address', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('email', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('searchList', djongo.models.fields.ArrayField(model_container=user.models.Search)),
            ],
        ),
    ]
