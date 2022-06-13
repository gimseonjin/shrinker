# Generated by Django 4.0.5 on 2022-06-13 07:14

import client.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('industry', models.CharField(choices=[('personal', 'Personal'), ('retail', 'Retail'), ('manufacturing', 'Manufacturing'), ('it', 'It'), ('others', 'Others')], default='others', max_length=15)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='client.organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShortenedUrls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nick_name', models.CharField(max_length=100)),
                ('prefix', models.CharField(max_length=50)),
                ('target_url', models.CharField(max_length=2000)),
                ('shortened_url', models.CharField(default=client.models.ShortenedUrls.rand_string, max_length=6)),
                ('create_via', models.CharField(choices=[('web', 'Website'), ('telegram', 'Telegram')], default='web', max_length=8)),
                ('expired_at', models.DateTimeField(null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='client.categories')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.users')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='pay_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='client.payplan'),
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=100, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.users')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='categories',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.users'),
        ),
        migrations.AddField(
            model_name='categories',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='client.organization'),
        ),
    ]
