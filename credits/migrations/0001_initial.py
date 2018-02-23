# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 01:11
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('access_type', models.IntegerField(blank=True, choices=[(1, 'Суперпользователь'), (2, 'Партнер'), (3, 'Кредитная организация')], null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время создания')),
                ('sent_at', models.DateTimeField(default=None, blank=True, null=True, verbose_name='Дата и время отправки')),
                ('status', models.CharField(choices=[('NEW', 'новая'), ('SENT', 'отправленная'), ('RECEIVED', 'принятая')], default=False, max_length=10, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заявка в кредитную организацию',
                'verbose_name_plural': 'Заявки в кредитные организации',
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время создания')),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время изменения')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('birth_day', models.DateField(verbose_name='День рождения')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Телефон')),
                ('passport_number', models.CharField(max_length=10, verbose_name='Номер паспорта')),
                ('score', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(850)], verbose_name='Скоринговый балл')),
            ],
            options={
                'verbose_name': 'Анкета клиента',
                'verbose_name_plural': 'Анкеты клиентов',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время создания')),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время изменения')),
                ('started_rotating_at', models.DateTimeField(verbose_name='Дата и время начала ротации')),
                ('ended_rotating_at', models.DateTimeField(verbose_name='Дата и время окончания ротации')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('category', models.CharField(choices=[('C', 'потребительский'), ('M', 'ипотека'), ('A', 'автокредит'), ('S', 'КМСБ')], max_length=1, verbose_name='Тип')),
                ('min_score', models.IntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(850)], verbose_name='Минимальны скоринговый балл')),
                ('max_score', models.IntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(850)], verbose_name='Максимальный скоринговый балл')),
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.AddField(
            model_name='offer',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.Organization'),
        ),
        migrations.AddField(
            model_name='application',
            name='customer_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.CustomerProfile', verbose_name='Анкета клиента'),
        ),
        migrations.AddField(
            model_name='application',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.Offer', verbose_name='Кредитное предложение'),
        ),
    ]
