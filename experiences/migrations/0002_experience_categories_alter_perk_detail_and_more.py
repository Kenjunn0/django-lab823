# Generated by Django 4.2.4 on 2023-09-07 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('experiences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category'),
        ),
        migrations.AlterField(
            model_name='perk',
            name='detail',
            field=models.CharField(blank=True, default='', max_length=140),
        ),
        migrations.AlterField(
            model_name='perk',
            name='name',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]