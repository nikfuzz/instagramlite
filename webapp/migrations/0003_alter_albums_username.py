# Generated by Django 4.0.3 on 2022-04-26 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_albums_username_alter_users_albumid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albums',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.users'),
        ),
    ]
