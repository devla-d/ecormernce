# Generated by Django 3.1.6 on 2021-02-16 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='country',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='state',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shoes'), ('SW', 'Sport wear'), ('HM', 'Home'), ('CR', 'Cars'), ('EL', 'Electronic'), ('BK', 'Books'), ('MP', 'mobile Phone'), ('mk', 'Makeup')], max_length=2),
        ),
    ]
