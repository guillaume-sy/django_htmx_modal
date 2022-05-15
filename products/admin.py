from django.contrib import admin

from.models import Product, Factory


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('product_name',
                    'product_reg_date',
                    'product_creating_user',
                    'product_factory_name')


class FactoryAdmin(admin.ModelAdmin):
    model = Factory
    list_display = ('factory_name',
                    'factory_reg_date',
                    'factory_creating_user',
                    'factory_long_coordinates',
                    'factory_lat_coordinates')


admin.site.register(Product, ProductAdmin)
admin.site.register(Factory, FactoryAdmin)

