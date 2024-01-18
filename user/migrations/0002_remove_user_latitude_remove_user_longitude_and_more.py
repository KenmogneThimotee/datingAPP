# Generated by Django 5.0.1 on 2024-01-17 21:48

import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='user',
            name='longitude',
        ),
        migrations.AddField(
            model_name='user',
            name='last_location',
            field=django.contrib.gis.db.models.fields.PointField(max_length=40, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_age_max',
            field=models.IntegerField(default=130, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(130)]),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_age_min',
            field=models.IntegerField(default=18, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(130)]),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_radius',
            field=models.IntegerField(default=5, help_text='in kilometers'),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], default='F', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], db_index=True, default='M', max_length=1),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
