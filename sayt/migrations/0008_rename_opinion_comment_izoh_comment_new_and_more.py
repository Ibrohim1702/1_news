# Generated by Django 4.1.6 on 2023-03-23 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayt', '0007_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='opinion',
            new_name='izoh',
        ),
        migrations.AddField(
            model_name='comment',
            name='new',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sayt.new'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
