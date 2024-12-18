# Generated by Django 4.2.16 on 2024-12-04 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demoapp', '0004_visitor_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='aboutpage',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='contactpage',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='contactpage',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='additional_comments',
            field=models.TextField(blank=True, null=True, verbose_name='Additional Comments'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visitors', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='favorite_thing_to_cook',
            field=models.CharField(max_length=255, verbose_name='Favorite Thing to Cook'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Phone'),
        ),
    ]
