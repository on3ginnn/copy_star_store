from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, RedirectView
from django.urls import reverse_lazy

from .models import Product, Category, Basket
from .forms import ProductCreateForm, CategoryCreateForm


class StoreHomepageView(TemplateView):
    template_name = "index.html"


class StoreCatalogView(ListView):
    queryset = Product.objects.filter(count_available__gt=0)
    template_name = 'catalog.html'
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Получаем параметр сортировки из GET
        sort_by = self.request.GET.get('filter_by', '')
        category_sort = self.request.GET.get('category_slug', '')

        if sort_by:
            sort_fields = {
                'new': '-created_at',
                'year': '-year_of_production',  # сначала новые года
                'year_old': 'year_of_production',  # сначала старые года
                'title': 'title',
                'title_desc': '-title', 
                'price': 'price',
                'price_desc': '-price',
            }
            field = sort_fields.get(sort_by, '-created_at')

            queryset = queryset.order_by(field)
        
        if category_sort:
            print(category_sort)
            print(queryset)
            queryset = queryset.filter(category__slug=category_sort)
            print(queryset)

        return queryset
        


class StoreProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = "product"


class StoreAdminProductCreateView(CreateView):
    model = Product
    template_name = 'admin/product_create.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy("store:admin-dashboard")


class StoreAdminCategoryCreateView(CreateView):
    model = Category
    template_name = 'admin/category_create.html'
    form_class = CategoryCreateForm
    success_url = reverse_lazy("store:admin-dashboard")


class StoreAdminDashboardView(TemplateView):
    template_name = "admin/dashboard.html"


class StoreBasketAddProductView(RedirectView):
    url = reverse_lazy("store:basket")

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)

        if product.count_available:
            # Используем get_or_create для поиска или создания корзины
            user_basket, created = Basket.objects.get_or_create(
                product=product,
                user=request.user,
            )

            if not created:
                user_basket.quantity += 1
                user_basket.save()

            product.count_available -= 1
            product.save()


        return super().get(request, *args, **kwargs)


class StoreBasketDeleteProductView(RedirectView):
    url = reverse_lazy("store:basket")

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)

        user_basket = get_object_or_404(Basket, product=product, user=request.user, )

        user_basket.quantity -= 1

        if not user_basket.quantity:
            user_basket.delete()
        else:
            user_basket.save()

        product.count_available += 1
        product.save()


        return super().get(request, *args, **kwargs)


class StoreBasketView(ListView):
    model = Basket
    template_name = "basket.html"
    context_object_name = 'basket_items'
    
    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)
    

class StoreAdminProductDeleteView(RedirectView):
    url = reverse_lazy("store:catalog")

    def get(self, request, *args, **kwargs):

        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)

        product.delete()

        return super().get(request, *args, **kwargs)
