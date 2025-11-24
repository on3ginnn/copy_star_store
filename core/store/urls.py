from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path("", StoreHomepageView.as_view(), name="homepage"),
    path("catalog/", StoreCatalogView.as_view(), name="catalog"),
    path("admin/dashboard/", StoreAdminDashboardView.as_view(), name="admin-dashboard"),
    path("admin/add/product/", StoreAdminProductCreateView.as_view(), name="admin-product"),
    path("admin/add/category/", StoreAdminCategoryCreateView.as_view(), name="admin-category"),
]