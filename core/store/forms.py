from django.forms import ModelForm

from .models import Product, Category, Basket


class ProductCreateForm(ModelForm):

    class Meta:
        model = Product
        fields = ['image', 'category', 'title', 'model', 'year_of_production', 'production_country', 'price', 'count_available']


class CategoryCreateForm(ModelForm):

    class Meta:
        model = Category
        fields = ['title']