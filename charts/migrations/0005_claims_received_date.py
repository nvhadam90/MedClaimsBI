# Generated by Django 4.0.2 on 2022-05-10 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0004_providers_city_providers_state_providers_tax_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='claims',
            name='received_date',
            field=models.DateField(null=True),
        ),
    ]