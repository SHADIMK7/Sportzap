# Generated by Django 4.2.7 on 2023-12-06 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0004_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turf_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner_app.turfbooking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner_app.customer')),
            ],
        ),
    ]
