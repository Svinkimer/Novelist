# Generated by Django 4.2.1 on 2023-08-09 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0002_alter_state_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrivalleave',
            name='img',
            field=models.ImageField(default='arrival/default.jpeg', upload_to='arrival/'),
        ),
        migrations.AlterField(
            model_name='location',
            name='img',
            field=models.ImageField(default='background/default.jpeg', upload_to='background/'),
        ),
        migrations.AlterField(
            model_name='my_user',
            name='img',
            field=models.ImageField(default='/user_icon/default.jpg', upload_to='user_icon/'),
        ),
        migrations.AlterField(
            model_name='state',
            name='img',
            field=models.ImageField(default='state/default.jpg', upload_to='state/'),
        ),
        migrations.AlterField(
            model_name='story',
            name='img',
            field=models.ImageField(default='poster/default.jpg', upload_to='poster/'),
        ),
    ]
