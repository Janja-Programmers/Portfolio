# Generated by Django 4.2.16 on 2024-11-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='mpesa_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
