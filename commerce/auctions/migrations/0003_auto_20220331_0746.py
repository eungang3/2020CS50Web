# Generated by Django 3.1.7 on 2022-03-31 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.URLField(blank=True, default='https://res.cloudinary.com/dxeibizaf/image/upload/v1616122317/auctions/29_ykmfm6.jpg'),
        ),
    ]
