# Generated by Django 5.1.5 on 2025-03-25 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(default='abc@gmail.com', max_length=254)),
                ('subject', models.CharField(default='Subject', max_length=300)),
                ('message', models.TextField(default='Message')),
            ],
        ),
    ]
