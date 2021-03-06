# Generated by Django 2.0.2 on 2018-03-24 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=100, verbose_name='中文名')),
                ('e_name', models.CharField(max_length=100, verbose_name='英文名')),
                ('school_type', models.CharField(max_length=100, verbose_name='学校类型')),
                ('address', models.CharField(max_length=100, verbose_name='学校地理位置')),
                ('TOEFL_score', models.CharField(max_length=100, verbose_name='托福成绩')),
                ('SAT_score', models.CharField(max_length=100, verbose_name='SAT成绩')),
                ('instructions', models.TextField(verbose_name='学校简介')),
            ],
        ),
    ]
