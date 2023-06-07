# Generated by Django 3.2.19 on 2023-06-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('guest', 'guest'), ('authorized', 'authorized'), ('admin', 'admin')], default='guest', max_length=10, verbose_name='Уровень доступа пользователей'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='Пользователь'),
        ),
    ]