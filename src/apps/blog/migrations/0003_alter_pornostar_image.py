# Generated by Django 4.1.8 on 2023-05-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_pornostar_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pornostar',
            name='image',
            field=models.ImageField(null=True, upload_to='star/%Y/%m/%d/'),
        ),
    ]