from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import Product, Category, Basket
from .forms import ProductCreateForm, CategoryCreateForm


class StoreHomepageView(TemplateView):
    template_name = "index.html"


class StoreCatalogView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = "products"


class StoreProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = "product"


class StoreAdminProductCreateView(CreateView):
    model = Product
    template_name = 'admin/product_create.html'
    form_class = ProductCreateForm


class StoreAdminCategoryCreateView(CreateView):
    model = Category
    template_name = 'admin/category_create.html'
    form_class = CategoryCreateForm


class StoreAdminDashboardView(TemplateView):
    template_name = "admin/dashboard.html"
