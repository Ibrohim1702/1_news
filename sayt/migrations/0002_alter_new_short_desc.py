# Generated by Django 4.1.6 on 2023-03-10 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='short_desc',
            field=models.CharField(max_length=512),
        ),
    ]
