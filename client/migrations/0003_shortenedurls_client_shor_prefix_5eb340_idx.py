# Generated by Django 4.0.5 on 2022-06-14 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_shortenedurls_prefix'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='shortenedurls',
            index=models.Index(fields=['prefix', 'shortened_url'], name='client_shor_prefix_5eb340_idx'),
        ),
    ]
