# Generated by Django 5.1.2 on 2024-10-13 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('face_encoding', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='attendance_images/')),
                ('status', models.CharField(max_length=50)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance_manager.person')),
            ],
        ),
    ]