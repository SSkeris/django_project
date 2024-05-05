from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.views import ProductListView, contacts, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, toggle_active

# пути для страниц на сайте
urlpatterns = [
                  path('', ProductListView.as_view(), name='product_list'),
                  path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
                  path('contacts/', contacts),
                  path('create/', ProductCreateView.as_view(), name='product_create'),
                  path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
                  path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
                  path('<int:pk>/active/', toggle_active, name='toggle_active'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
