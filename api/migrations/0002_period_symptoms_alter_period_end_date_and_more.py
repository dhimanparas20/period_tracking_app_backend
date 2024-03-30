# Generated by Django 5.0.2 on 2024-03-30 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='symptoms',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='period',
            name='end_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='period',
            name='start_date',
            field=models.DateField(blank=True),
        ),
        migrations.DeleteModel(
            name='Symptom',
        ),
    ]