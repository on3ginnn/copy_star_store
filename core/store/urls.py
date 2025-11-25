from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path("", StoreHomepageView.as_view(), name="homepage"),
    path("catalog/", StoreCatalogView.as_view(), name="catalog"),
    path("detail/<int:pk>/", StoreProductDetailView.as_view(), name="detail"),
    path("basket/add/<int:pk>/", StoreBasketAddProductView.as_view(), name="add-basket"),
    path("basket/delete/<int:pk>/", StoreBasketDeleteProductView.as_view(), name="delete-basket"),
    path("basket/", StoreBasketView.as_view(), name="basket"),
    path("admin/dashboard/", StoreAdminDashboardView.as_view(), name="admin-dashboard"),
    path("admin/add/product/", StoreAdminProductCreateView.as_view(), name="admin-product"),
    path("admin/add/category/", StoreAdminCategoryCreateView.as_view(), name="admin-category"),
    path("admin/delete/product/<int:pk>/", StoreAdminProductDeleteView.as_view(), name="delete-product"),
]