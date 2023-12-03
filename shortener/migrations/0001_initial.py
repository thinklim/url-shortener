# Generated by Django 4.2.7 on 2023-12-03 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortener.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, default='', max_length=500)),
                ('prefix', models.CharField(default=shortener.models.ShortenedUrl.get_random_letter, max_length=50)),
                ('source_url', models.URLField(max_length=1000)),
                ('target_url', models.CharField(default=shortener.models.ShortenedUrl.get_random_string, max_length=7)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'shortened_url',
                'indexes': [models.Index(fields=['name'], name='shortened_u_name_d347df_idx'), models.Index(fields=['prefix'], name='shortened_u_prefix_64bea4_idx'), models.Index(fields=['source_url'], name='shortened_u_source__e39ec8_idx'), models.Index(fields=['target_url'], name='shortened_u_target__3451db_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='shortenedurl',
            constraint=models.UniqueConstraint(fields=('prefix', 'target_url'), name='unique_shortened_url'),
        ),
    ]
