# Generated by Django 3.1.7 on 2022-04-01 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220331_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bidder',
        ),
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
