# Generated by Django 4.2.1 on 2023-06-06 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('crm', '0004_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ForeignKey(choices=[(5, 'Vente'), (4, 'Gestion'), (6, 'Support')], max_length=30, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group', verbose_name='team'),
        ),
    ]
