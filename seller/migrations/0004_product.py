# Generated by Django 4.1.5 on 2023-01-30 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('des', models.CharField(max_length=250)),
                ('price', models.DecimalField(decimal_places=3, default=500, max_digits=10)),
                ('pic', models.FileField(default='pro_def_img.jpg', upload_to='product_images')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]
