# Generated by Django 2.2.1 on 2020-02-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20200216_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='合同名称')),
                ('content', models.TextField(verbose_name='合同内容')),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
