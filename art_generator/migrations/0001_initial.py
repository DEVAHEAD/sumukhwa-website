# Generated by Django 4.2 on 2023-05-10 02:32

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
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now=True)),
                ('projectName', models.CharField(default='devahead', max_length=100)),
                ('negativePrompt', models.CharField(default='', max_length=100)),
                ('positivePrompt', models.CharField(default='', max_length=100)),
                ('projectType', models.CharField(default='1', max_length=100)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': ['created'],
            },
        ),
        migrations.CreateModel(
            name='GeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now=True)),
                ('selected', models.BooleanField(default=False)),
                ('image', models.ImageField(default='generated/test1.jpg', upload_to='uploads/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art_generator.project')),
            ],
        ),
    ]
