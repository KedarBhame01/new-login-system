# Generated by Django 5.2.1 on 2025-07-25 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
