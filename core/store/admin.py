from django.contrib import admin

from .models import Category, Product, Basket


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    # prepopulated_fields = {'slug': ('title',)}  # работает только в админке


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
