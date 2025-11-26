from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path("", StoreHomepageView.as_view(), name="homepage"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("catalog/", StoreCatalogView.as_view(), name="catalog"),
    path("detail/<int:pk>/", StoreProductDetailView.as_view(), name="detail"),
    path("basket/add/<int:pk>/", StoreBasketAddProductView.as_view(), name="add-basket"),
    path("basket/delete/<int:pk>/", StoreBasketDeleteProductView.as_view(), name="delete-basket"),
    path("basket/", StoreBasketView.as_view(), name="basket"),
    # Orders (client)
    path("orders/checkout/", CheckoutFormView.as_view(), name="checkout"),
    path("orders/", MyOrdersListView.as_view(), name="orders"),
    path("orders/delete/<int:pk>/", MyOrderDeleteView.as_view(), name="order-delete"),
    path("admin/dashboard/", StoreAdminDashboardView.as_view(), name="admin-dashboard"),
    # Orders (admin)
    path("admin/orders/", AdminOrdersListView.as_view(), name="admin-orders"),
    path("admin/orders/<int:pk>/confirm/", AdminOrderConfirmView.as_view(), name="admin-order-confirm"),
    path("admin/orders/<int:pk>/cancel/", AdminOrderCancelView.as_view(), name="admin-order-cancel"),
    path("admin/add/product/", StoreAdminProductCreateView.as_view(), name="admin-product"),
    path("admin/add/category/", StoreAdminCategoryCreateView.as_view(), name="admin-category"),
    path("admin/delete/product/<int:pk>/", StoreAdminProductDeleteView.as_view(), name="delete-product"),
]