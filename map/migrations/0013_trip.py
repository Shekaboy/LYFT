# Generated by Django 3.1.1 on 2020-10-26 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('map', '0012_auto_20201026_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.event')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='beavers', to='login.beaver')),
            ],
        ),
    ]
