# Generated by Django 4.2.1 on 2023-08-10 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_alter_arrivalleave_img_alter_location_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrivalleave',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrival', to='editor.sceneevent'),
        ),
    ]
