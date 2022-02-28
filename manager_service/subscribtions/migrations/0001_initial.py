# Generated by Django 4.0.2 on 2022-02-16 23:40

import datetime
import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.TextField(choices=[('Active', 'Active'), ('Overdue', 'Overdue'), ('Canceled', 'Canceled')], verbose_name='Статус подписки')),
                ('payment_token', models.TextField(blank=True, null=True, verbose_name='Платежный токен')),
                ('expiration_dt', models.DateField(blank=True, null=True, verbose_name='Дата окончания подписки')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, choices=[('Subscriber', 'Subscriber')], max_length=256, verbose_name='Название подписки')),
                ('description', models.TextField(blank=True, null=True)),
                ('period', models.DurationField(choices=[(datetime.timedelta(days=8), 'Week'), (datetime.timedelta(days=7), 'Month'), (datetime.timedelta(days=6), 'Year')], default=datetime.timedelta(days=7), verbose_name='Период подписки')),
                ('amount', models.PositiveIntegerField(blank=True, verbose_name='Цена подписки')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.TextField(choices=[('Paid', 'Paid'), ('In work', 'In Work'), ('Not paid', 'Not Paid')], verbose_name='Статус подписки')),
                ('amount', models.PositiveIntegerField(blank=True, verbose_name='Сумма к оплате')),
                ('paid_period', models.DurationField(blank=True, verbose_name='Оплачиваемый период')),
                ('due_dt', models.DateField(blank=True, verbose_name='Срок оплаты')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills', to='subscribtions.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='account',
            name='tariff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='subscribtions.tariff'),
        ),
    ]
