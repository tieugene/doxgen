# Generated by Django 3.1.2 on 2021-01-16 13:09

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
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('method', models.BooleanField(verbose_name='Метод')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('path', models.CharField(max_length=255, verbose_name='Куда')),
                ('agent', models.CharField(max_length=255, null=True, verbose_name='Агент')),
                ('data', models.TextField(verbose_name='Данные')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('type', models.CharField(max_length=32, verbose_name='Тип')),
                ('name', models.CharField(max_length=32, verbose_name='Наименование')),
                ('data', models.TextField(verbose_name='Данные')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'ordering': ('type', 'name'),
                'unique_together': {('user', 'type', 'name')},
            },
        ),
    ]