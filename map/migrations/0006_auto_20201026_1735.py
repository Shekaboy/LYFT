# Generated by Django 3.1.1 on 2020-10-26 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_remove_event_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='people',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(blank=True, default='images/default/event.jpeg', help_text='Event Photo', null=True, upload_to='images/events/'),
        ),
    ]
