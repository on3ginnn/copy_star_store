from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, RedirectView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponseForbidden

from .models import Product, Category, Basket, Order, OrderItem
from .forms import ProductCreateForm, CategoryCreateForm


class StoreHomepageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = Product.objects.order_by("-created_at")[:5]
        return ctx


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



class StoreAdminProductCreateView(UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'admin/product_create.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy("store:admin-dashboard")
    login_url = reverse_lazy('account:login')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff



class StoreAdminCategoryCreateView(UserPassesTestMixin, CreateView):
    model = Category
    template_name = 'admin/category_create.html'
    form_class = CategoryCreateForm
    success_url = reverse_lazy("store:admin-dashboard")
    login_url = reverse_lazy('account:login')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff



class StoreAdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "admin/dashboard.html"
    login_url = reverse_lazy('account:login')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


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
        return Basket.objects.filter(user=self.request.user).select_related('product')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = ctx['basket_items']
        ctx['total_items'] = sum(item.quantity for item in items)
        ctx['total_price'] = sum(item.get_total_price() for item in items)
        return ctx
    


class StoreAdminProductDeleteView(UserPassesTestMixin, RedirectView):
    url = reverse_lazy("store:catalog")
    login_url = reverse_lazy('account:login')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return super().get(request, *args, **kwargs)


class ContactsView(TemplateView):
    template_name = "contacts.html"


class CheckoutFormView(LoginRequiredMixin, TemplateView):
    template_name = "orders/checkout.html"
    success_url = reverse_lazy("store:orders")

    def get(self, request, *args, **kwargs):
        basket_qs = Basket.objects.filter(user=request.user)
        if not basket_qs.exists():
            return redirect("store:basket")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password = request.POST.get("password", "")
        user = authenticate(username=request.user.username, password=password)
        if not user:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": False, "error": "Неверный пароль"}, status=400)
            context = {"error": "Неверный пароль"}
            return render(request, self.template_name, context, status=400)

        basket_items = Basket.objects.filter(user=request.user)
        if not basket_items.exists():
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": False, "error": "Корзина пуста"}, status=400)
            return redirect("store:basket")

        order = Order.objects.create(user=request.user)
        for item in basket_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        basket_items.delete()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "redirect": str(self.success_url)})

        return redirect(self.success_url)


class MyOrdersListView(LoginRequiredMixin, ListView):
    template_name = "orders/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class MyOrderDeleteView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("store:orders")

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"), user=request.user)
        if order.status == Order.Status.NEW:
            order.restore_stock()
            order.delete()
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Нельзя удалить заказ со статусом не 'Новый'")


class AdminOrdersListView(UserPassesTestMixin, ListView):
    template_name = "admin/orders_list.html"
    context_object_name = "orders"

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_queryset(self):
        qs = Order.objects.select_related("user").prefetch_related("items")
        status = self.request.GET.get("status")
        if status in {s.value for s in Order.Status}:
            qs = qs.filter(status=status)
        return qs.order_by("-created_at")


class AdminOrderConfirmView(UserPassesTestMixin, RedirectView):
    url = reverse_lazy("store:admin-orders")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))
        order.status = Order.Status.CONFIRMED
        order.cancelled_reason = ""
        order.save()
        return super().get(request, *args, **kwargs)


class AdminOrderCancelView(UserPassesTestMixin, TemplateView):
    template_name = "admin/order_cancel.html"
    success_url = reverse_lazy("store:admin-orders")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["order"] = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        return ctx

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))
        reason = request.POST.get("reason", "").strip()
        if order.status != Order.Status.CANCELLED:
            order.restore_stock()
        order.status = Order.Status.CANCELLED
        order.cancelled_reason = reason[:255]
        order.save()
        return redirect(self.success_url)
