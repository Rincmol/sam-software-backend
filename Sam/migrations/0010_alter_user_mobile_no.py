# Generated by Django 3.2.7 on 2021-09-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0009_ledger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_no',
            field=models.CharField(max_length=100),
        ),
    ]