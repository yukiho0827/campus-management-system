# Generated by Django 4.0.1 on 2022-04-23 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_alter_placelibrary_create_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceBasketballGround',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('stu_number', models.CharField(max_length=32, verbose_name='学号')),
                ('phone_number', models.CharField(max_length=32, verbose_name='手机号')),
                ('create_time', models.DateTimeField(verbose_name='时间')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceDiningRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('stu_number', models.CharField(max_length=32, verbose_name='学号')),
                ('phone_number', models.CharField(max_length=32, verbose_name='手机号')),
                ('create_time', models.DateTimeField(verbose_name='时间')),
            ],
        ),
    ]
