# Generated by Django 4.1 on 2023-03-03 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0006_alter_book_isbn_alter_issuedbook_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.PositiveIntegerField(verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 17, 15, 41, 3, 525743), verbose_name='Expires in:'),
        ),
    ]
