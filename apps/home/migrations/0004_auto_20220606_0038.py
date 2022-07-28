# Generated by Django 3.2.11 on 2022-06-05 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20220602_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlmodels',
            name='metric',
        ),
        migrations.AddField(
            model_name='mlmodels',
            name='Precision',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mlmodels',
            name='Recall',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mlmodels',
            name='accuracy',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mlmodels',
            name='confusion_matrix',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mlmodels',
            name='f1',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mlmodels',
            name='model_file',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='mlmodels',
            name='scaler_file',
            field=models.TextField(),
        ),
    ]