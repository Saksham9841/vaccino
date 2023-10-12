# Generated by Django 4.2.1 on 2023-06-22 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_color_remove_product_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='color_variant',
            field=models.ManyToManyField(blank=True, to='store.colorvariant'),
        ),
        migrations.AddField(
            model_name='order',
            name='size_variant',
            field=models.ManyToManyField(blank=True, to='store.sizevariant'),
        ),
    ]