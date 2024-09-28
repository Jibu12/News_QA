# Generated by Django 5.1.1 on 2024-09-16 06:41

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('n_app', '0003_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('views_count', models.IntegerField(default=0)),
                ('likes_count', models.IntegerField(default=0)),
                ('shares_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('trending_score', models.IntegerField(default=0)),
                ('tags', models.CharField(blank=True, max_length=255)),
                ('author_name', models.CharField(blank=True, max_length=255)),
                ('meta_description', models.TextField(blank=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('cover_image', models.URLField(blank=True)),
                ('news_image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='n_app.category')),
                ('subcategory_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='n_app.subcategory')),
            ],
        ),
    ]
