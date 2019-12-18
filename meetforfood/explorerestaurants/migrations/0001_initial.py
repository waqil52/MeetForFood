
# Generated by Django 2.1.7 on 2019-12-18 20:25

from django.db import migrations, models
import django.db.models.deletion
import explorerestaurants.models
import multiselectfield.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=120)),
                ('item_image', models.ImageField(blank=True, default=None, max_length=254, null=True, upload_to=explorerestaurants.models.nameFileMenu)),
                ('serving', models.IntegerField()),
                ('price', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[('Bangladeshi', 'Bangladeshi'), ('Chinese', 'Chinese'), ('Indian', 'Indian'), ('Italian', 'Italian'), ('Thai', 'Thai'), ('Japanese', 'Japanese'), ('Korean', 'Korean'), ('Fast_Food', 'Fast Food'), ('Juice_Bar', 'Juice Bar'), ('Coffee_Shop', 'Coffee Shop'), ('IceCream_Shop', 'Ice Cream Shop'), ('Buffet', 'Buffet'), ('Turkish', 'Turkish'), ('Bakery', 'Bakery'), ('Cake_Shop', 'Cake Shop')], default='Bangladeshi', max_length=100)),
                ('price_category', models.CharField(choices=[('$', 'Affordable'), ('$$', 'Inexpensive'), ('$$$', 'Expensive'), ('$$$$', 'Posh')], default='$', max_length=4)),
                ('restaurant_image', models.ImageField(blank=True, default=None, max_length=254, null=True, upload_to=explorerestaurants.models.nameFileRestaurant)),
                ('address', models.CharField(max_length=460)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
        ),
        migrations.AddField(
            model_name='menuinfo',
            name='restaurant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorerestaurants.RestaurantInfo'),
        migrations.CreateModel(
            name='MenuInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=120)),
                ('category_name', models.CharField(default=None, max_length=40)),
                ('serving', models.CharField(max_length=10)),
                ('price', models.CharField(max_length=10)),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorerestaurants.RestaurantInfo')),
            ],
        ),
    ]
