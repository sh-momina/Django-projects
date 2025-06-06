# Generated by Django 5.1.1 on 2024-11-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WEB', '0009_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('image_data', models.BinaryField()),
                ('content_type', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
